from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QGridLayout

class AutoView(QWidget):
    def __init__(self, controller, user_controller=None, dashboard_view=None, parent=None):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.user_controller = user_controller
        self.setWindowTitle('Auto Management')
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        if parent:
            self.setGeometry(parent.geometry())
        self.setLayout(self.main_layout)
        self.populateAuto()
        self.centerWindow()

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

    def populateAuto(self):
        # Rimuove tutti i widget dal layout principale
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        # Bottone per tornare alla Dashboard
        dashboard_btn = QPushButton('Torna alla Dashboard')
        dashboard_btn.setObjectName('dashboard_button')
        dashboard_btn.clicked.connect(self.goToDashboard)
        self.main_layout.addWidget(dashboard_btn)

        # Recupera il ruolo dell'utente
        role = self.user_controller.getRuoloUtente()
        is_admin = role == 'amministratore'
        

        # Area auto
        auto_frame = QFrame()
        auto_frame.setObjectName('auto_frame')
        grid_auto_layout = QGridLayout(auto_frame)

        for i, auto in enumerate(self.controller.getAutoVisibili()):
            auto_widget = QWidget()
            auto_widget.setObjectName('auto_widget')
            auto_layout = QVBoxLayout(auto_widget)
            auto_layout.setContentsMargins(10, 10, 10, 10)

            # Label auto
            auto_layout.addWidget(QLabel(f"Marca: {auto['marca']}"))
            auto_layout.addWidget(QLabel(f"Modello: {auto['modello']}"))
            auto_layout.addWidget(QLabel(f"Anno: {auto['anno']}"))
            auto_layout.addWidget(QLabel(f"Chilometri: {auto['chilometri']}"))
            auto_layout.addWidget(QLabel(f"Prezzo: {auto['prezzo']}€"))
            auto_layout.addWidget(QLabel(f"Targa: {auto['targa']}"))

            # Bottoni solo per amministratore
            
            elimina_auto_btn = QPushButton('Elimina Auto')
            elimina_auto_btn.setObjectName('elimina_auto_button')
            elimina_auto_btn.clicked.connect(
                lambda _, id=auto['id']: self.controller.eliminaAuto(id, self)
            )
            auto_layout.addWidget(elimina_auto_btn)

            modifica_auto_btn = QPushButton('Modifica Auto')
            modifica_auto_btn.setObjectName('modifica_auto_button')
            modifica_auto_btn.clicked.connect(
                lambda _, a=auto: self.controller.modificaAutoDialog(
                    a['id'], a['marca'], a['modello'], a['anno'], a['chilometri'], a['prezzo'], a['targa'], self
                )
            )
            auto_layout.addWidget(modifica_auto_btn)
            elimina_auto_btn.setVisible(is_admin)
            modifica_auto_btn.setVisible(is_admin)

            grid_auto_layout.addWidget(auto_widget, i // 4, i % 4)

        self.main_layout.addWidget(auto_frame)
        self.main_layout.addStretch()

        
        create_auto_btn = QPushButton('Crea Auto')
        create_auto_btn.setObjectName('create_auto_button')
        create_auto_btn.clicked.connect(self.controller.creaAutoDialog)
        self.main_layout.addWidget(create_auto_btn)
        create_auto_btn.setVisible(is_admin)

    def refreshAuto(self):
        """Aggiorna la visualizzazione delle auto"""
        self.populateAuto()

    def goToDashboard(self):
        self.hide()
        self.dashboard_view.show()

    def centerWindow(self):
        """Centra la finestra sullo schermo"""
        screen = self.screen().availableGeometry()
        self.move(
            max(0, (screen.width() - self.width()) // 2),
            max(0, (screen.height() - self.height()) // 2)
        )
 