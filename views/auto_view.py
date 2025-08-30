from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame, QGridLayout, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt
from controllers.auto_controller import AutoController

class AutoView(QWidget):
    def __init__(self, controller, auth_controller=None, dashboard_view=None, parent=None):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.auth_controller = auth_controller
        self.setWindowTitle('Auto Management')
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        if parent:
            self.setGeometry(parent.geometry())
        self.setLayout(self.main_layout)
        self.populate_auto()
        self.controller.center_window(self)

        # Stile uguale a ContractView
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
            QPushButton#dashboard_button {
                background-color: black;
                max-width: 200px;
                min-height: 50px;
                font-size: 20px;
            }
            QFrame#auto_frame {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 10px;
            }
            QWidget#auto_widget {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton#elimina_auto_button {
                background-color: #e74c3c;
            }
            QPushButton#elimina_auto_button:hover {
                background-color: #c0392b;
            }
            QPushButton#modifica_auto_button {
                background-color: #2980b9;
            }
            QPushButton#modifica_auto_button:hover {
                background-color: #1f6391;
            }
            QPushButton#create_auto_button {
                background-color: black;
                min-height: 40px;
                font-size: 20px;
            }
        """)

    def populate_auto(self):
        # Pulisce layout principale
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Bottone Dashboard
        dashboard_btn = QPushButton('Torna alla Dashboard')
        dashboard_btn.setObjectName('dashboard_button')
        dashboard_btn.clicked.connect(self.go_to_dashboard)
        button_layout = QHBoxLayout()
        button_layout.addWidget(dashboard_btn)
        button_layout.addStretch()
        self.main_layout.addLayout(button_layout)

        role = self.auth_controller.get_current_user_data().get('ruolo', 'cliente')
        is_admin = role == 'amministratore'

        # ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_layout.addWidget(scroll_area)

        # Frame auto
        auto_frame = QFrame()
        auto_frame.setObjectName('auto_frame')
        grid_auto_layout = QGridLayout(auto_frame)

        for i, auto in enumerate(self.controller.get_all_auto()):
            auto_widget = QWidget()
            auto_widget.setObjectName('auto_widget')
            auto_layout = QVBoxLayout(auto_widget)
            auto_layout.setContentsMargins(10, 10, 10, 10)
            auto_layout.setSpacing(5)

            # Labels
            auto_layout.addWidget(QLabel(f"Marca: {auto['marca']}"))
            auto_layout.addWidget(QLabel(f"Modello: {auto['modello']}"))
            auto_layout.addWidget(QLabel(f"Anno: {auto['anno']}"))
            auto_layout.addWidget(QLabel(f"Chilometri: {auto['chilometri']}"))
            auto_layout.addWidget(QLabel(f"Prezzo: {auto['prezzo']}"))
            auto_layout.addWidget(QLabel(f"Targa: {auto['targa']}"))

            # Pulsanti Admin
            elimina_auto_btn = QPushButton('Elimina Auto')
            elimina_auto_btn.setObjectName('elimina_auto_button')
            elimina_auto_btn.clicked.connect(lambda _, id=auto['id']: self.controller.elimina_auto(id, self))
            modifica_auto_btn = QPushButton('Modifica Auto')
            modifica_auto_btn.setObjectName('modifica_auto_button')
            modifica_auto_btn.clicked.connect(lambda _, a=auto: self.controller.modificaAuto(
                a['id'], a['marca'], a['modello'], a['anno'], a['chilometri'], a['prezzo'], a['targa'], self
            ))
            auto_layout.addWidget(elimina_auto_btn)
            auto_layout.addWidget(modifica_auto_btn)
            elimina_auto_btn.setVisible(is_admin)
            modifica_auto_btn.setVisible(is_admin)

            grid_auto_layout.addWidget(auto_widget, i // 4, i % 4)

        scroll_area.setWidget(auto_frame)

        # Pulsante Crea Auto Admin
        create_auto_btn = QPushButton('Crea Auto')
        create_auto_btn.setObjectName('create_auto_button')
        create_auto_btn.clicked.connect(self.controller.crea_auto_dialog)
        create_auto_btn.setVisible(is_admin)
        self.main_layout.addWidget(create_auto_btn)

    def refresh_auto(self):
        self.populate_auto()

    def go_to_dashboard(self):
        self.hide()
        self.dashboard_view.show()
