from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette

class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.register_view = None
        self.dashboard_view = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Sistema di Login')
        #self.setFixedSize(500, 450)
        
        
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Titolo
        title = QLabel('Accedi al tuo account')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Frame per il form
        form_frame = QFrame()
        form_frame.setObjectName('form_frame')
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
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
        self.login_button.setObjectName('primary_button')
    #self.login_button.clicked.connect(
    #lambda: self.controller.handle_login(self.username_input.text(), self.password_input.text(), self))
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        main_layout.addWidget(form_frame)
        
        # Link registrazione
        register_layout = QHBoxLayout()
        register_label = QLabel("Non hai un account?")
        self.register_button = QPushButton('Registrati qui')
        self.register_button.setObjectName('link_button')
        self.register_button.clicked.connect(self.controller.show_register)
        
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_button)
        register_layout.addStretch()
        
        main_layout.addLayout(register_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Connessione Enter per login
        
    #self.password_input.returnPressed.connect(lambda: self.controller.handle_login(self.username_input.text(), self.password_input.text(), self))
        self.password_input.returnPressed.connect(self.handle_login)

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
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.controller.handle_login(username, password, self):
            self.show_dashboard()

    def show_dashboard(self):
        from controllers.dashboard_controller import DashboardController
        from views.dashboard_view import DashboardView

        dashboard_controller = DashboardController(self.controller)
        self.dashboard_view = DashboardView(dashboard_controller)
        self.dashboard_view.show()
        self.hide()
    
    