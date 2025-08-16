from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QGridLayout, QLineEdit, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

from models.auto_model import AutoModel
from models.contract_model import ContractModel
from controllers.fatture_controller import FattureController
from views.fatture_view import FattureView


class ContractView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('ContractView')
        self.init_ui()


    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        contract_frame = QFrame()
        contract_frame.setObjectName('contract_frame')
        contract_grid_layout = QGridLayout(contract_frame)

        contracts = self.controller.get_all_contracts()

        for i, contract in enumerate(contracts):
            contract_widget = QWidget()
            contract_widget.setObjectName('contract_widget')
            contract_layout = QVBoxLayout(contract_widget)
            contract_layout.setContentsMargins(10, 10, 10, 10)
        
            user_label = QLabel(f"User: {contract['user']}")
            auto_label = QLabel(f"auto: {contract['auto']}")
            start_date_label = QLabel(f"start date: {contract['start_date']}")
            end_date_label = QLabel(f"end date: {contract['end_date']}")
            price_label = QLabel(f"Price: {contract['price']}")

            contract_layout.addWidget(user_label)
            contract_layout.addWidget(auto_label)
            contract_layout.addWidget(start_date_label)
            contract_layout.addWidget(end_date_label)
            contract_layout.addWidget(price_label)


            view_fatture_btn = QPushButton('Visualizza Fatture')
            view_fatture_btn.setObjectName('view_fatture_button')
            view_fatture_btn.clicked.connect(lambda checked, c=contract: self.show_fatture_view(c))

            contract_layout.addWidget(view_fatture_btn)

            contract_grid_layout.addWidget(contract_widget, i // 4, i % 4)

        main_layout.addWidget(contract_frame)
        main_layout.addStretch()
        
        crea_contract_btn = QPushButton('crea contratto')
        crea_contract_btn.setObjectName('crea_contratto_button')
        crea_contract_btn.clicked.connect(self.controller.crea_contratto)

        main_layout.addWidget(crea_contract_btn)

        self.setLayout(main_layout)
        
        # Centra la finestra
        self.controller.center_window(self)
            
    def show_fatture_view(self, contract):
        fatture_controller = FattureController(self.controller, contract)
        self.fatture_view = FattureView(fatture_controller, contract)
        self.fatture_view.setWindowTitle(f"Fatture per il contratto: {contract['id']}")
        self.fatture_view.show()
    
    def refresh_contracts(self):
        """Aggiorna la visualizzazione dei contratti"""
        # Rimuovi tutti i widget dal layout principale
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        # Ricrea l'interfaccia
        self.init_ui()

    