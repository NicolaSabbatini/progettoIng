from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QDateEdit, QComboBox
from PyQt5.QtCore import Qt, QDate

from models.Auto import Auto

class CreaContrattoNoleggioDialog(QDialog):
    def __init__(self, parent=None, controller=None, contract_view=None):
        super().__init__(parent)
        self.controller = controller
        self.contract_view = contract_view
        self.setWindowTitle('Crea un nuovo contratto')
        self.setFixedSize(750,850)

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
            QComboBox {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 30px;
                color: white;
            }
            QComboBox:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #2e86de;
                border-radius: 3px;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: none;
                background-color: transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #2e86de;
                border: 1px solid #bbb;
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
        
        layout = QVBoxLayout(self)
        
        user_input = QLineEdit()
        user_input.setPlaceholderText('user')
        layout.addWidget(QLabel('user:'))
        layout.addWidget(user_input)

        auto_model = Auto()
        auto_list = auto_model.get_all_auto()
        
        auto_combo = QComboBox()
        auto_combo.setObjectName('auto_combo')
        for auto in auto_list:
            display_text = f"{auto['marca']} {auto['modello']} ({auto['anno']}) - {auto['targa']}"
            auto_combo.addItem(display_text, auto['id'])
        layout.addWidget(QLabel('Seleziona auto:'))
        layout.addWidget(auto_combo)

        start_date_input = QDateEdit()
        start_date_input.setCalendarPopup(True)
        start_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel('start date:'))
        layout.addWidget(start_date_input)

        end_date_input = QDateEdit()
        end_date_input.setCalendarPopup(True)
        end_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel('end date:'))
        layout.addWidget(end_date_input)

        cauzione_input = QLineEdit()
        cauzione_input.setPlaceholderText('cauzione')
        layout.addWidget(QLabel('cauzione:'))
        layout.addWidget(cauzione_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo:'))
        layout.addWidget(prezzo_input)

        durataGaranzia_input = QLineEdit()
        durataGaranzia_input.setPlaceholderText('durata garanzia')
        layout.addWidget(QLabel('durata garanzia:'))
        layout.addWidget(durataGaranzia_input)

        tipoGaranzia_input = QLineEdit()
        tipoGaranzia_input.setPlaceholderText('tipo garanzia')
        layout.addWidget(QLabel('tipo garanzia:'))
        layout.addWidget(tipoGaranzia_input)

        kmMax_input = QLineEdit()
        kmMax_input.setPlaceholderText('chilometri massimi')
        layout.addWidget(QLabel('chilometri massimi:'))
        layout.addWidget(kmMax_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva contratto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_contract(user_input,auto_combo,start_date_input,end_date_input,cauzione_input,prezzo_input, durataGaranzia_input, tipoGaranzia_input, kmMax_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_contract(self,user_input,auto_combo,start_date_input,end_date_input,cauzione_input,prezzo_input, durataGaranzia_input, tipoGaranzia_input, kmMax_input):
        user = user_input.text()
        auto = auto_combo.currentData()
        start_date = start_date_input.text()
        end_date = end_date_input.text()
        cauzione = cauzione_input.text()
        prezzo = prezzo_input.text()
        durataGaranzia = durataGaranzia_input.text()
        tipoGaranzia = tipoGaranzia_input.text()
        kmMax = kmMax_input.text()



        if user and auto and start_date and end_date and cauzione and prezzo and durataGaranzia and tipoGaranzia and kmMax:
            self.controller.addo_noleggio_contratto(user, auto, start_date, end_date, cauzione, tipoGaranzia, durataGaranzia, kmMax, prezzo)
            self.accept()

        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
