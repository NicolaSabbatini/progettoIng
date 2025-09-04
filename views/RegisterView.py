from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QLineEdit, QPushButton, QMessageBox,
                              QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QDate
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
            QDateEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 30px;
                color: white;
            }
            QDateEdit:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #2e86de;
                border-radius: 3px;
                width: 20px;
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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)

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

        form_frame = QFrame()
        form_frame.setObjectName('form_frame')
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(30, 30, 30, 30)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Inserisci il tuo nome")
        form_layout.addWidget(QLabel("Nome:"))
        form_layout.addWidget(self.nome_input)

        self.cognome_input = QLineEdit()
        self.cognome_input.setPlaceholderText("Inserisci il tuo cognome")
        form_layout.addWidget(QLabel("Cognome:"))
        form_layout.addWidget(self.cognome_input)

        self.luogo_input = QLineEdit()
        self.luogo_input.setPlaceholderText("Inserisci il tuo luogo di nascita")
        form_layout.addWidget(QLabel("Luogo di Nascita:"))
        form_layout.addWidget(self.luogo_input)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Inserisci il tuo numero di telefono")
        form_layout.addWidget(QLabel("Telefono:"))
        form_layout.addWidget(self.telefono_input)

        self.data_nascita_input = QDateEdit()
        self.data_nascita_input.setCalendarPopup(True)
        self.data_nascita_input.setDate(QDate.currentDate())
        form_layout.addWidget(QLabel("Data di Nascita:"))
        form_layout.addWidget(self.data_nascita_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Scegli un username")
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Inserisci la tua email")
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Minimo 6 caratteri")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)

        self.conferma_password_input = QLineEdit()
        self.conferma_password_input.setPlaceholderText("Ripeti la password")
        self.conferma_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel("Conferma Password:"))
        form_layout.addWidget(self.conferma_password_input)

        # Bottone registrazione
        self.register_button = QPushButton('Registrati')
        self.register_button.setObjectName('primary_button')
        self.register_button.clicked.connect(self.handleRegister)
        form_layout.addWidget(self.register_button)

        form_wrapper = QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_frame)
        form_wrapper.addStretch()
        content_layout.addLayout(form_wrapper)

        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        self.back_button = QPushButton('← Torna al Login')
        self.back_button.setObjectName('link_button')
        self.back_button.clicked.connect(self.backToLogin)
        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()
        content_layout.addLayout(nav_layout)

        self.conferma_password_input.returnPressed.connect(self.handleRegister)

        self.centerWindow()

    def centerWindow(self):
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def handleRegister(self):
        success, message = self.controller.register(
            self.username_input.text(),
            self.email_input.text(),
            self.password_input.text(),
            self.conferma_password_input.text(),
            self.nome_input.text(),
            self.cognome_input.text(),
            self.luogo_input.text(),
            self.telefono_input.text(),
            self.data_nascita_input.text()
        )

        if success:
            QMessageBox.information(self, 'Successo', message)
            self.backToLogin()
        else:
            QMessageBox.warning(self, 'Errore di Registrazione', message)

    def backToLogin(self):
        self.login_view.clearFields()
        self.login_view.show()
        self.hide()
