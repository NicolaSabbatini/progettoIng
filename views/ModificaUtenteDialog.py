from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit

class ModificaUtenteDialog(QDialog):
    def __init__(self, controller, utente_data, parent=None, dashboard_view=None):
        super().__init__(parent)
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.username = utente_data["username"]

        self.setWindowTitle('Modifica Utente')
        self.setFixedSize(600, 800)
        layout = QVBoxLayout(self)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: Arial;
                font-size: 18px;
            }
            QLabel {
                background-color: #2b2b2b;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 1px solid #2e86de;
                background-color: black;
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
            QPushButton#secondary_button {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#secondary_button:hover {
                background-color: #c0392b;
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

        # Campi precompilati
        self.name_input = QLineEdit(utente_data.get("name", ""))
        layout.addWidget(QLabel('Nome:'))
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit(utente_data.get("surname", ""))
        layout.addWidget(QLabel('Cognome:'))
        layout.addWidget(self.surname_input)

        #self.username_input = QLineEdit(utente_data.get("username", ""))
        #layout.addWidget(QLabel('Username:'))
        #layout.addWidget(self.username_input)



        self.old_password_input = QLineEdit("")
        layout.addWidget(QLabel('Vecchia Password:'))
        layout.addWidget(self.old_password_input)

        self.new_password_input = QLineEdit("")
        layout.addWidget(QLabel('Nuova Password:'))
        layout.addWidget(self.new_password_input)

        self.email_input = QLineEdit(utente_data.get("email", ""))
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email_input)

        self.luogo_input = QLineEdit(utente_data.get("luogo", ""))
        layout.addWidget(QLabel('Luogo:'))
        layout.addWidget(self.luogo_input)

        self.telefono_input = QLineEdit(utente_data.get("telefono", ""))
        layout.addWidget(QLabel('Telefono:'))
        layout.addWidget(self.telefono_input)

        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel('Data di nascita:'))
        layout.addWidget(self.data_input)

        # Bottone per salvare le modifiche
        save_btn = QPushButton('Salva Modifiche')
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(self.salvaModifiche)


        role = self.controller.getRuoloUtente()
        if role == 'cliente':
            # Bottone per eliminare il profilo
            delete_btn = QPushButton('Elimina Profilo')
            delete_btn.setObjectName('secondary_button')
            layout.addWidget(delete_btn)
            delete_btn.clicked.connect(self.eliminaProfilo)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def salvaModifiche(self):
        """Aggiorna i dati dell’utente con i nuovi valori"""

        name = self.name_input.text()
        surname = self.surname_input.text()
        username = self.username
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        email = self.email_input.text()
        luogo = self.luogo_input.text()
        telefono = self.telefono_input.text()
        data = self.data_input.text()

        if name and surname and username and email and luogo and telefono and data:
            success, message = self.controller.aggiornaUtente(
                self.username,
                old_password,
                new_password,  # può essere None
                name,
                surname,
                email,
                luogo,
                telefono,
                data
            )
            if success:
                if self.dashboard_view:
                    self.dashoboard_view.refreshUtente()
                QMessageBox.information(self, "Successo", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Errore", message)
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')

    
        
    def eliminaProfilo(self):
        """Elimina il profilo dell'utente"""
        reply = QMessageBox.question(
            self,
            'Conferma Eliminazione',
            'Sei sicuro di voler eliminare il tuo profilo? Questa azione è irreversibile.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success, message = self.controller.eliminaUtente(self.username)
            if success:
                QMessageBox.information(self, "Successo", message)
                self.accept()  # chiudi il dialog
            else:
                QMessageBox.warning(self, "Errore", message)
                    