from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from controllers.fatture_controller import FattureController
from views.fatture_view import FattureView

class ContractView(QWidget):
    def __init__(self, controller, dashboard_view):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.setWindowTitle('ContractView')
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setFixedSize(700,550)
        self.setLayout(self.main_layout)
        self.populate_contracts()
        self.controller.center_window(self)

    def populate_contracts(self):
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
            garanzia_label = QLabel(f"Garanzia: {contract['garanzia']}")

            contract_layout.addWidget(user_label)
            contract_layout.addWidget(auto_label)
            contract_layout.addWidget(start_date_label)
            contract_layout.addWidget(end_date_label)
            contract_layout.addWidget(price_label)
            contract_layout.addWidget(garanzia_label)

            view_fatture_btn = QPushButton('Visualizza Fatture')
            view_fatture_btn.setObjectName('view_fatture_button')
            view_fatture_btn.clicked.connect(lambda checked, c=contract: self.show_fatture_view(c))
            
            elimina_contract_btn = QPushButton('elimina contratto')
            elimina_contract_btn.setObjectName('elimina_contratto_button')
            elimina_contract_btn.clicked.connect(lambda: self.controller.delete_contract_and_fatture(contract['id'], self))
            
            contract_layout.addWidget(view_fatture_btn)
            contract_layout.addWidget(elimina_contract_btn)

            contract_grid_layout.addWidget(contract_widget, i // 4, i % 4)

            
            
        

        self.main_layout.addWidget(contract_frame)
        self.main_layout.addStretch()

        crea_contract_btn = QPushButton('crea contratto')
        crea_contract_btn.setObjectName('crea_contratto_button')
        crea_contract_btn.clicked.connect(self.controller.crea_contratto)
        self.main_layout.addWidget(crea_contract_btn)

        

    def show_fatture_view(self, contract):
        fatture_controller = FattureController(self.controller, contract, fatture_view=self)
        self.fatture_view = FattureView(fatture_controller, contract)
        self.fatture_view.setWindowTitle(f"Fatture per il contratto: {contract['id']}")
        self.fatture_view.show()

    def refresh_contracts(self):
        self.populate_contracts()

    def go_to_dashboard(self):
        self.hide()
        self.dashboard_view.show()
    