from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame, QGridLayout

from controllers.auto_controller import AutoController


class AutoView(QWidget):
    def __init__(self, controller, dashboard_view=None):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.setWindowTitle('Auto Management')
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setFixedSize(700,550)
        self.setLayout(self.main_layout)
        self.populate_auto()
        self.controller.center_window(self)



       



    def populate_auto(self):
        # Rimuovi tutti i widget dal layout principale
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        
        
        
        dashboard_btn = QPushButton('Torna alla Dashboard')
        dashboard_btn.setObjectName('dashboard_button')
        dashboard_btn.clicked.connect(self.go_to_dashboard)
        self.main_layout.addWidget(dashboard_btn)
        
        # Area auto
        auto_frame = QFrame()
        auto_frame.setObjectName('auto_frame')
        grid_auto_layout = QGridLayout(auto_frame)
        
        for i, auto in enumerate(self.controller.get_all_auto()):
            auto_widget = QWidget()
            auto_widget.setObjectName('auto_widget')
            auto_layout = QVBoxLayout(auto_widget)
            auto_layout.setContentsMargins(10, 10, 10, 10)
    
            marca_label = QLabel(f"Marca: {auto['marca']}")
            modello_label = QLabel(f"Modello: {auto['modello']}")
            anno_label = QLabel(f"Anno: {auto['anno']}")
            chilometri_label = QLabel(f"Chilometri: {auto['chilometri']}")
            prezzo_label = QLabel(f"Prezzo: {auto['prezzo']}")
            targa_label = QLabel(f"Targa: {auto['targa']}")

            
    
            auto_layout.addWidget(marca_label)
            auto_layout.addWidget(modello_label)
            auto_layout.addWidget(anno_label)
            auto_layout.addWidget(chilometri_label)
            auto_layout.addWidget(prezzo_label)
            auto_layout.addWidget(targa_label)
    

            elimina_auto_btn = QPushButton('elimina auto')
            elimina_auto_btn.setObjectName('elimina_auto_button')
            elimina_auto_btn.clicked.connect(lambda: self.controller.elimina_auto(auto['id'], self))
            
            auto_layout.addWidget(elimina_auto_btn)

            grid_auto_layout.addWidget(auto_widget, i // 4, i % 4)


        # Bottone per creare una nuova auto
        create_auto_btn = QPushButton('Crea Auto') 
        create_auto_btn.setObjectName('create_auto_button')
        create_auto_btn.clicked.connect(self.controller.crea_auto_dialog)

        self.main_layout.addWidget(auto_frame)
        self.main_layout.addStretch()
        self.main_layout.addWidget(create_auto_btn)

    def refresh_auto(self):
        """Aggiorna la visualizzazione delle auto"""
        self.populate_auto()

    
    def go_to_dashboard(self):
        self.hide()
        self.dashboard_view.show()