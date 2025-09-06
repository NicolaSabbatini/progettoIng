from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout, QPushButton, QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy

class FattureView(QWidget):
    def __init__(self, controller, contract, role = 'cliente', parent =None):
        super().__init__()
        self.controller = controller
        self.contract = contract
        self.role = role
        self.setWindowTitle('Fatture per il Contratto')
        if parent:
            self.setGeometry(parent.geometry())

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)

        if parent:
            self.setGeometry(parent.geometry())

        

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 18px;
            }
            QPushButton {
                background-color: black;
                color: white;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton#crea_fattura_button {
                background-color: #2980b9;
                
            }
            QPushButton#crea_fattura_button:hover {
                background-color: #1f6391;
            }
            QFrame#fatture_widget {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
            }
            QFrame#fatture_frame {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 10px;
            }
        """)


        self.populateFatture()
        self.centerWindow()

    def populateFatture(self):
        # Rimuove i widget precedenti dalla layout
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Frame che contiene le fatture
        fatture_frame = QFrame()
        fatture_frame.setObjectName('fatture_frame')
        grid_fatture_layout = QGridLayout(fatture_frame)
        grid_fatture_layout.setContentsMargins(20, 20, 20, 20)
        grid_fatture_layout.setSpacing(15)

        fatture_list = self.controller.getFatturePerContratto(self.contract['id'])

        for i, fattura in enumerate(fatture_list):
            fatture_widget = QWidget()
            fatture_widget.setObjectName('fatture_widget')
            fatture_layout = QVBoxLayout(fatture_widget)
            fatture_layout.setContentsMargins(10, 10, 10, 20)

            # dimensione fissa
            fatture_widget.setFixedSize(420, 100)

            data_label = QLabel(f"Data: {fattura['data']}")
            prezzo_label = QLabel(f"Prezzo: {fattura['prezzo']}€")

            fatture_layout.addWidget(data_label)
            fatture_layout.addWidget(prezzo_label)

            # inserisco nella griglia (max 4 colonne per riga)
            grid_fatture_layout.addWidget(
                fatture_widget,
                i // 4,  # riga
                i % 4,   # colonna
                alignment=Qt.AlignTop | Qt.AlignLeft
            )

        # IMPORTANTISSIMO: impedisco alla griglia di "stirare" le colonne
        for col in range(4):
            grid_fatture_layout.setColumnStretch(col, 0)

        # Scroll area che contiene tutto
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(fatture_frame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setMaximumHeight(900)

        self.main_layout.addWidget(scroll_area)
        self.main_layout.addStretch()

        # Bottone solo per admin
        if self.role == 'amministratore':
            crea_fattura_button = QPushButton('Crea Fattura')
            crea_fattura_button.setObjectName('crea_fattura_button')
            crea_fattura_button.setFixedWidth(150)
            crea_fattura_button.clicked.connect(self.createFattura)

            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(crea_fattura_button)
            button_layout.addStretch()

            button_container = QWidget()
            button_container.setLayout(button_layout)

            self.main_layout.addWidget(button_container)

    def createFattura(self):
        # Call the controller to create a fattura, then refresh the view
        self.controller.creaFatturaDialog(self.contract['id'])
        self.populateFatture()

    def centerWindow(self):
        screen = self.screen().availableGeometry()
        self.move(
            max(0, (screen.width() - self.width()) // 2),
            max(0, (screen.height() - self.height()) // 2)
        )

    def refreshFatture(self):
        self.populateFatture()