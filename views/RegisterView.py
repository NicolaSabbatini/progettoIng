from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RegisterView(QWidget):
    def __init__(self, controller, login_view, parent=None):
        super().__init__()
        self.controller = controller
        self.login_view = login_view
        if parent:
            self.setGeometry(parent.geometry())

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: Arial;
                font-size: 18px;
            }
            #form_frame {
                background-color: black;
                border: 1px solid #dcdcdc;
                border-radius: 12px;
            }
            QLabel {
                background-color: black;
            }
            QLabel#title {
                color: #2e86de;
                font-size: 33px;
                background-color: #2b2b2b;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 40px;
            }
            QLineEdit:focus {
                border: 1px solid #2e86de;
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

        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Registrazione')
        self.resize(900, 900)
        
        main_layout = QVBoxLayout(self)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)

        # Contenitore scroll
        scroll_content = QWidget()
        scroll.setWidget(scroll_content)

        content_layout = QVBoxLayout(scroll_content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 30, 40, 30)

        # Titolo
        title = QLabel('Crea un nuovo account')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        content_layout.addWidget(title)

        # Frame form
        form_frame = QFrame()
        form_frame.setObjectName('form_frame')
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Campi input
        fields = [
            ("Nome:", "Inserisci il tuo nome"),
            ("Cognome:", "Inserisci il tuo cognome"),
            ("Luogo di Nascita:", "Inserisci il tuo luogo di nascita"),
            ("Telefono:", "Inserisci il tuo numero di telefono"),
            ("Data di Nascita:", "YYYY-MM-DD"),
            ("Username:", "Scegli un username"),
            ("Email:", "Inserisci la tua email"),
            ("Password:", "Minimo 6 caratteri", True),
            ("Conferma Password:", "Ripeti la password", True)
        ]

        self.inputs = {}

        for field in fields:
            label = QLabel(field[0])
            input_field = QLineEdit()
            input_field.setPlaceholderText(field[1])
            input_field.setMinimumHeight(40)  # altezza maggiore
            if len(field) == 3 and field[2]:
                input_field.setEchoMode(QLineEdit.Password)
            form_layout.addWidget(label)
            form_layout.addWidget(input_field)
            self.inputs[field[0]] = input_field

        # Bottone registrazione
        self.register_button = QPushButton('Registrati')
        self.register_button.setObjectName('primary_button')
        self.register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_button)

        # Centra il form
        form_wrapper = QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_frame)
        form_wrapper.addStretch()
        content_layout.addLayout(form_wrapper)

        # Bottoni navigazione
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        self.back_button = QPushButton('← Torna al Login')
        self.back_button.setObjectName('link_button')
        self.back_button.clicked.connect(self.back_to_login)
        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()
        content_layout.addLayout(nav_layout)

        # Enter su conferma password
        self.inputs["Conferma Password:"].returnPressed.connect(self.handle_register)

        # Applica stile QSS (uguale a LoginView)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: Arial;
                font-size: 18px;
            }
            #form_frame {
                background-color: black;
                border: 1px solid #dcdcdc;
                border-radius: 12px;
            }
            QLabel {
                background-color: black;
            }
            QLabel#title {
                color: #2e86de;
                font-size: 33px;
                background-color: #2b2b2b;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 40px;
            }
            QLineEdit:focus {
                border: 1px solid #2e86de;
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
        self.center_window()

    def center_window(self):
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def handle_register(self):
        data = {label: field.text() for label, field in self.inputs.items()}

        success, message = self.controller.register(
            data["Username:"],
            data["Email:"],
            data["Password:"],
            data["Conferma Password:"],
            data["Nome:"],
            data["Cognome:"],
            data["Luogo di Nascita:"],
            data["Telefono:"],
            data["Data di Nascita:"]
        )

        if success:
            QMessageBox.information(self, 'Successo', message)
            self.back_to_login()
        else:
            QMessageBox.warning(self, 'Errore di Registrazione', message)

    def back_to_login(self):
        self.login_view.clear_fields()
        self.login_view.show()
        self.hide()
