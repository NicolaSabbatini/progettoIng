from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit)
from PyQt5.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self, controller, login_view):
        super().__init__()
        self.controller = controller
        self.login_view = login_view
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Dashboard')
        #self.setFixedSize(600, 400)
        #self.setStyleSheet(self.get_stylesheet())
        
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel('Benvenuto!')
        self.welcome_label.setObjectName('welcome_title')
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        
        self.logout_button = QPushButton('Logout')
        self.logout_button.setObjectName('logout_button')
        self.logout_button.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.logout_button)
        
        main_layout.addLayout(header_layout)
        
        # Frame informazioni utente
        info_frame = QFrame()
        info_frame.setObjectName('info_frame')
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
        info_title = QLabel('Informazioni Account')
        info_title.setObjectName('section_title')
        info_layout.addWidget(info_title)
        
        # Campi informazioni
        self.username_label = QLabel()
        self.email_label = QLabel()
        self.created_label = QLabel()
        self.login_time_label = QLabel()
        self.username_label.setObjectName('info_label')
        self.email_label.setObjectName('info_label')
        self.created_label.setObjectName('info_label')
        self.login_time_label.setObjectName('info_label')
        self.name_label = QLabel()
        self.name_label.setObjectName('info_label')
        self.surname_label = QLabel()
        self.surname_label.setObjectName('info_label')
        self.luogo_label = QLabel()
        self.luogo_label.setObjectName('info_label')
        self.telefono_label = QLabel()
        self.telefono_label.setObjectName('info_label')
        self.data_label = QLabel()
        self.data_label.setObjectName('info_label')
        self.update_user_info()
       
        
        info_layout.addWidget(self.username_label)
        info_layout.addWidget(self.email_label)
        info_layout.addWidget(self.created_label)
        info_layout.addWidget(self.login_time_label)
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.surname_label)
        info_layout.addWidget(self.luogo_label)
        info_layout.addWidget(self.telefono_label)
        info_layout.addWidget(self.data_label)
        info_layout.addStretch()

        
        main_layout.addWidget(info_frame)
        
        # Area note (esempio di funzionalità aggiuntiva)
        notes_frame = QFrame()
        notes_frame.setObjectName('info_frame')
        notes_layout = QVBoxLayout(notes_frame)
        
        notes_title = QLabel('Note Personali')
        notes_title.setObjectName('section_title')
        notes_layout.addWidget(notes_title)
        
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText('Scrivi le tue note qui...')
        self.notes_text.setMaximumHeight(100)
        notes_layout.addWidget(self.notes_text)
        
        main_layout.addWidget(notes_frame)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Centra la finestra
        self.center_window()
    
    def get_stylesheet(self):
        return """
            QWidget {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #welcome_title {
                font-size: 28px;
                font-weight: bold;
            }
            
            #section_title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            
            #info_frame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 20px;
            }
            
            #info_frame QLabel {
                color: #333;
                font-size: 14px;
                padding: 5px 0;
            }
            
            #logout_button {
                background-color: #e53e3e;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            
            #logout_button:hover {
                background-color: #c53030;
            }
            
            QTextEdit {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 6px;
                color: #333;
                font-size: 14px;
                padding: 10px;
            }
            
            QTextEdit:focus {
                border-color: #667eea;
            }
        """
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def update_user_info(self):
        """Aggiorna le informazioni utente nella dashboard"""
        user_data = self.controller.get_current_user_data()
        
        if user_data:
            self.welcome_label.setText(f'Benvenuto, {user_data["username"]}!')
            self.username_label.setText(f'👤 Username: {user_data["username"]}')
            self.email_label.setText(f'📧 Email: {user_data["email"]}')
            self.created_label.setText(f'📅 Account creato: {user_data["created_at"]}')
            self.login_time_label.setText(f'🕐 Ultimo accesso: {user_data["login_time"]}')
            self.name_label.setText(f'Nome: {user_data.get("name", "N/A")}')
            self.surname_label.setText(f'Cognome: {user_data.get("surname", "N/A")}')
            self.luogo_label.setText(f'Luogo: {user_data.get("luogo", "N/A")}')
            self.telefono_label.setText(f'Telefono: {user_data.get("telefono", "N/A")}')
            self.data_label.setText(f'Data di nascita: {user_data.get("data", "N/A")}')
            
    
    def handle_logout(self):
        """Gestisce il logout"""
        self.controller.logout()
        self.login_view.clear_fields()
        self.login_view.show()
        self.hide()