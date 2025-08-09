from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt

class RegisterView(QWidget):
    def __init__(self, controller, login_view):
        super().__init__()
        self.controller = controller
        self.login_view = login_view
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Registrazione')
        #self.setFixedSize(450, 400)
        
        
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)
        
        # Titolo
        title = QLabel('Crea un nuovo account')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Frame per il form
        form_frame = QFrame()
        form_frame.setObjectName('form_frame')
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(12)
        
        # Campo nome
        name_label = QLabel('Nome:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Inserisci il tuo nome')     
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)  

        # Campo cognome
        surname_label = QLabel('Cognome:')                  
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText('Inserisci il tuo cognome')
        form_layout.addWidget(surname_label)
        form_layout.addWidget(self.surname_input)
        
        # Campo luogo
        luogo_label = QLabel('Luogo di Nascita:')   
        self.luogo_input = QLineEdit()
        self.luogo_input.setPlaceholderText('Inserisci il tuo luogo di nascita')
        form_layout.addWidget(luogo_label)
        form_layout.addWidget(self.luogo_input)

        # Campo telefono
        telefono_label = QLabel('Telefono:') 
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText('Inserisci il tuo numero di telefono')
        form_layout.addWidget(telefono_label)
        form_layout.addWidget(self.telefono_input)

        # Campo data di nascita
        data_label = QLabel('Data di Nascita:') 
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText('Inserisci la tua data di nascita (YYYY-MM-DD)')
        form_layout.addWidget(data_label)   
        form_layout.addWidget(self.data_input)
        
        


        # Campo username
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Scegli un username')
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        
        # Campo email
        email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Inserisci la tua email')
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        
        # Campo password
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Minimo 6 caratteri')
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        # Campo conferma password
        confirm_label = QLabel('Conferma Password:')
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText('Ripeti la password')
        form_layout.addWidget(confirm_label)
        form_layout.addWidget(self.confirm_input)
        
        # Bottone registrazione
        self.register_button = QPushButton('Registrati')
        self.register_button.setObjectName('primary_button')
        self.register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_button)
        
        main_layout.addWidget(form_frame)
        
        # Bottoni navigazione
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton('← Torna al Login')
        self.back_button.setObjectName('secondary_button')
        self.back_button.clicked.connect(self.back_to_login)
        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()
        
        main_layout.addLayout(nav_layout)
        
        self.setLayout(main_layout)
        
        # Connessione Enter
        self.confirm_input.returnPressed.connect(self.handle_register)
        
        # Centra la finestra
        self.center_window()
    
    
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def handle_register(self):
        """Gestisce la registrazione"""
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_input.text()
        name = self.name_input.text()
        surname = self.surname_input.text()
        luogo = self.luogo_input.text()
        telefono = self.telefono_input.text()
        data = self.data_input.text()

        
        success, message = self.controller.register(username, email, password, confirm_password, name, surname, luogo, telefono, data)
        
        if success:
            QMessageBox.information(self, 'Successo', message)
            self.back_to_login()
        else:
            QMessageBox.warning(self, 'Errore di Registrazione', message)
    
    def back_to_login(self):
        """Torna alla schermata di login"""
        self.login_view.clear_fields()
        self.login_view.show()
        self.hide()