from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout, QPushButton, QScrollArea, QSizePolicy, QHBoxLayout
)
from PyQt5.QtCore import Qt

class FattureView(QWidget):
    def __init__(self, controller, contract, role='cliente', parent=None):
        super().__init__()
        self.controller = controller
        self.contract = contract
        self.role = role
        self.setWindowTitle(f'Fatture per il Contratto: {contract["id"]}')
        self.resize(1100, 900)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)

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

        self.populate_fatture()
        self.center_window()

    def populate_fatture(self):
        # Clear previous content
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_layout.addWidget(scroll_area)

        # Container for fatture
        fatture_frame = QFrame()
        fatture_frame.setObjectName('fatture_frame')
        scroll_area.setWidget(fatture_frame)
        grid_fatture_layout = QGridLayout(fatture_frame)

        fatture_list = self.controller.get_fatture_by_contratto(self.contract['id'])
        for i, fattura in enumerate(fatture_list):
            fatture_widget = QFrame()
            fatture_widget.setObjectName('fatture_widget')
            fatture_layout = QVBoxLayout(fatture_widget)
            fatture_layout.setContentsMargins(10, 10, 10, 10)
            fatture_layout.setSpacing(8)

            fatture_layout.addWidget(QLabel(f"ID Fattura: {fattura['idfattura']}"))
            fatture_layout.addWidget(QLabel(f"Contratto: {fattura['contratto']}"))
            fatture_layout.addWidget(QLabel(f"Data: {fattura['data']}"))
            fatture_layout.addWidget(QLabel(f"Prezzo: {fattura['prezzo']}"))

            grid_fatture_layout.addWidget(fatture_widget, i // 4, i % 4)

        if self.role == 'amministratore':
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()
            crea_fattura_button = QPushButton('Crea Fattura')
            crea_fattura_button.setObjectName('crea_fattura_button')
            crea_fattura_button.clicked.connect(self.create_fattura)
            btn_layout.addWidget(crea_fattura_button)
            btn_layout.addStretch()
            self.main_layout.addLayout(btn_layout)

        #self.main_layout.addStretch()

    def create_fattura(self):
        self.controller.create_fattura_button(self.contract['id'])
        self.populate_fatture()

    def center_window(self):
        screen = self.screen().availableGeometry()
        self.move(
            max(0, (screen.width() - self.width()) // 2),
            max(0, (screen.height() - self.height()) // 2)
        )
