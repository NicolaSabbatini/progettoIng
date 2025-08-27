from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from controllers.fatture_controller import FattureController
from views.fatture_view import FattureView

class ContractView(QWidget):
    def __init__(self, controller, dashboard_view, auth_controller=None):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.auth_controller = auth_controller
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
        self.controller.contract_model.load_contracts()  # ricarica i dati da file
        role = self.auth_controller.get_current_user_data().get('ruolo', 'cliente')
        if role == 'amministratore':
            contracts = self.controller.get_all_contracts()
        else:
            contracts = self.controller.get_contracts(self.auth_controller.get_current_user_data().get('username'))

        rent_contracts = [c for c in contracts if c.get('tipo') == 'noleggio']
        buy_contracts = [c for c in contracts if c.get('tipo') == 'acquisto']
        
        print("contratti totali: ")
        for c in contracts:
            print(c)
        print("contratti acquisto: ")
        for c in buy_contracts:
            print(c)
        print("contratti noleggio: ")
        for c in rent_contracts:
            print(c)

        for i, contract in enumerate(rent_contracts):
            contract_widget = QWidget()
            contract_widget.setObjectName('contract_widget')
            contract_layout = QVBoxLayout(contract_widget)
            contract_layout.setContentsMargins(10, 10, 10, 10)
        
            user_label = QLabel(f"User: {contract['user']}")
            auto_label = QLabel(f"auto: {contract['auto']}")
            start_date_label = QLabel(f"start date: {contract['start_date']}")
            end_date_label = QLabel(f"end date: {contract['end_date']}")
            cauzione_label = QLabel(f"cauzione: {contract['cauzione']}")
            price_label = QLabel(f"Price: {contract['prezzoTot']}")
            tipoGaranzia_label = QLabel(f"tipo garanzia: {contract['tipoGaranzia']}")
            durataGaranzia_label = QLabel(f"durata garanzia: {contract['durataGaranzia']}")
            kmMax_label = QLabel(f"chilometri massimi: {contract['kmMax']}")

            contract_layout.addWidget(user_label)
            contract_layout.addWidget(auto_label)
            contract_layout.addWidget(start_date_label)
            contract_layout.addWidget(end_date_label)
            contract_layout.addWidget(price_label)
            contract_layout.addWidget(tipoGaranzia_label)
            contract_layout.addWidget(durataGaranzia_label)
            contract_layout.addWidget(cauzione_label)
            contract_layout.addWidget(kmMax_label)

            view_fatture_btn = QPushButton('Visualizza Fatture')
            view_fatture_btn.setObjectName('view_fatture_button')
            view_fatture_btn.clicked.connect(lambda checked, c=contract: self.show_fatture_view(c))
            contract_layout.addWidget(view_fatture_btn)

            if role == 'amministratore':
                elimina_contract_btn = QPushButton('elimina contratto')
                elimina_contract_btn.setObjectName('elimina_contratto_button')
                elimina_contract_btn.clicked.connect(
                    lambda checked=False, c=contract: self.controller.delete_contract_and_fatture(c['id'], c['auto'], self))
                contract_layout.addWidget(elimina_contract_btn)

            contract_grid_layout.addWidget(contract_widget, i // 4, i % 4)



        for i, contract in enumerate(buy_contracts):
            contract_widget = QWidget()
            contract_widget.setObjectName('contract_widget')
            contract_layout = QVBoxLayout(contract_widget)
            contract_layout.setContentsMargins(10, 10, 10, 10)
        
            user_label = QLabel(f"User: {contract['user']}")
            auto_label = QLabel(f"auto: {contract['auto']}")
            price_label = QLabel(f"Price: {contract['price']}")
            tipoGaranzia_label = QLabel(f"tipo garanzia: {contract['tipoGaranzia']}")
            durataGaranzia_label = QLabel(f"durata garanzia: {contract['durataGaranzia']}")

            contract_layout.addWidget(user_label)
            contract_layout.addWidget(auto_label)
            contract_layout.addWidget(price_label)
            contract_layout.addWidget(tipoGaranzia_label)
            contract_layout.addWidget(durataGaranzia_label)

            if role == 'amministratore':
                elimina_contract_btn = QPushButton('elimina contratto')
                elimina_contract_btn.setObjectName('elimina_contratto_button')
                elimina_contract_btn.clicked.connect(
                    lambda checked=False, c=contract: self.controller.elimina_contratto(c['id'], self))
                contract_layout.addWidget(elimina_contract_btn)
            
            contract_grid_layout.addWidget(contract_widget, (i + len(rent_contracts)) // 4, (i + len(rent_contracts)) % 4)

            
            
        

        self.main_layout.addWidget(contract_frame)
        self.main_layout.addStretch()
        if role == 'amministratore':
            crea_acquisto_contract_btn = QPushButton('crea contratto acquisto')
            crea_acquisto_contract_btn.setObjectName('crea_contratto_acquisto_button')
            crea_acquisto_contract_btn.clicked.connect(self.controller.crea_acquisto_contratto)
            self.main_layout.addWidget(crea_acquisto_contract_btn)

            crea_noleggio_contract_btn = QPushButton('crea contratto noleggio')
            crea_noleggio_contract_btn.setObjectName('crea_contratto_noleggio_button')
            crea_noleggio_contract_btn.clicked.connect(self.controller.crea_noleggio_contratto)
            self.main_layout.addWidget(crea_noleggio_contract_btn)

        

    def show_fatture_view(self, contract):
        role = self.auth_controller.get_current_user_role()
        fatture_controller = FattureController(self.controller, contract, fatture_view=self)
        self.fatture_view = FattureView(fatture_controller, contract, role)
        self.fatture_view.setWindowTitle(f"Fatture per il contratto: {contract['id']}")
        self.fatture_view.show()

    def refresh_contracts(self):
        self.populate_contracts()

    def go_to_dashboard(self):
        self.hide()
        self.dashboard_view.show()
    