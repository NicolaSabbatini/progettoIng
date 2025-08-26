from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame, QGridLayout

from controllers.auto_controller import AutoController

class AutoView(QWidget):
    def __init__(self, controller, auth_controller=None, dashboard_view=None):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.auth_controller = auth_controller
        self.setWindowTitle('Auto Management')
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setFixedSize(700, 550)
        self.setLayout(self.main_layout)
        self.populate_auto()
        self.controller.center_window(self)

    def populate_auto(self):
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
        dashboard_btn.clicked.connect(self.go_to_dashboard)
        self.main_layout.addWidget(dashboard_btn)

        # Recupera il ruolo dell'utente
        role = self.auth_controller.get_current_user_data().get('ruolo', 'cliente')
        is_admin = role == 'amministratore'
        

        # Area auto
        auto_frame = QFrame()
        auto_frame.setObjectName('auto_frame')
        grid_auto_layout = QGridLayout(auto_frame)

        for i, auto in enumerate(self.controller.get_all_auto()):
            auto_widget = QWidget()
            auto_widget.setObjectName('auto_widget')
            auto_layout = QVBoxLayout(auto_widget)
            auto_layout.setContentsMargins(10, 10, 10, 10)

            # Label auto
            auto_layout.addWidget(QLabel(f"Marca: {auto['marca']}"))
            auto_layout.addWidget(QLabel(f"Modello: {auto['modello']}"))
            auto_layout.addWidget(QLabel(f"Anno: {auto['anno']}"))
            auto_layout.addWidget(QLabel(f"Chilometri: {auto['chilometri']}"))
            auto_layout.addWidget(QLabel(f"Prezzo: {auto['prezzo']}"))
            auto_layout.addWidget(QLabel(f"Targa: {auto['targa']}"))

            # Bottoni solo per amministratore
            
            elimina_auto_btn = QPushButton('Elimina Auto')
            elimina_auto_btn.setObjectName('elimina_auto_button')
            elimina_auto_btn.clicked.connect(
                lambda _, id=auto['id']: self.controller.elimina_auto(id, self)
            )
            auto_layout.addWidget(elimina_auto_btn)

            modifica_auto_btn = QPushButton('Modifica Auto')
            modifica_auto_btn.setObjectName('modifica_auto_button')
            modifica_auto_btn.clicked.connect(
                lambda _, a=auto: self.controller.modificaAuto(
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
        create_auto_btn.clicked.connect(self.controller.crea_auto_dialog)
        self.main_layout.addWidget(create_auto_btn)
        create_auto_btn.setVisible(is_admin)

    def refresh_auto(self):
        """Aggiorna la visualizzazione delle auto"""
        self.populate_auto()

    def go_to_dashboard(self):
        self.hide()
        self.dashboard_view.show()
 