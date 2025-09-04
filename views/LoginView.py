from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt



class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.register_view = None
        self.dashboard_view = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Sistema di Login')
        self.setMinimumSize(500, 450)

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(60, 60, 60, 60)
        
        # Titolo
        title = QLabel('Accedi al tuo account')
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Frame per il form
        form_frame = QFrame()
        form_frame.setObjectName("form_frame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)
        
        # Campo username
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Inserisci il tuo username')
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        
        # Campo password
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Inserisci la tua password')
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        # Bottone login
        self.login_button = QPushButton('Accedi')
        self.login_button.setObjectName("primary_button")
        self.login_button.clicked.connect(self.handleLogin)
        form_layout.addWidget(self.login_button)
        
        form_wrapper = QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_frame)
        form_wrapper.addStretch()
        main_layout.addLayout(form_wrapper)

        
        # Link registrazione
        register_layout = QHBoxLayout()
        register_label = QLabel("Non hai un account?")
        register_label.setObjectName("register_label")
        self.register_button = QPushButton('Registrati qui')
        self.register_button.setObjectName("link_button")
        self.register_button.clicked.connect(self.controller.visualizzaRegistrazione)
        
        register_layout.addStretch()
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_button)
        register_layout.addStretch()
        
        main_layout.addLayout(register_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Connessione Enter per login
        self.password_input.returnPressed.connect(self.handleLogin)

        # Applica stile CSS
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b; /* grigio scuro */
                color: white; /* testo bianco */
                font-family: Arial;
                font-size: 20px;
            }
            #form_frame {
                background-color: black;
                border: 1px solid #dcdcdc;
                border-radius: 12px;
                max-width: 1000px;
                min-height: 300px;
            }
            QLabel {
                background-color: black;
            }
            QLabel#title {
                color: #2e86de;
                background-color: #2b2b2b; /* grigio scuro */
                font-size: 33px;
                font-style: arial;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
            }
            QLineEdit:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QPushButton#primary_button {
                background-color: #2e86de;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#primary_button:hover {
                background-color: #1b4f72;
            }
            QLabel#register_label{
                background-color: #2b2b2b;
            }
            QPushButton#link_button {
                background: none;
                color: #2e86de;
                border: none;
                text-decoration: underline;
            }
            QPushButton#link_button:hover {
                color: #1b4f72;
            }
            QMessageBox {
            background-color: #2b2b2b;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            }
            QMessageBox QLabel {
                color: white;
                background-color: #2b2b2b;
                font-size: 18px;
            }
            QMessageBox QPushButton {
                background-color: #2e86de;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1b4f72;
            }
            """)


        # Centra la finestra
        self.centerWindow()
    
    
    def centerWindow(self):
        """Centra la finestra sullo schermo"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def handleLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.controller.login(username, password, self):
            self.controller.visualizzaDashboard(username)

    

    def clearFields(self):
        """Pulisce i campi di input"""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()

    
    