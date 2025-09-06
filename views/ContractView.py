from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QHBoxLayout, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt

from controllers.GestoreAuto import GestoreAuto
from views.FattureView import FattureView

class ContractView(QWidget):
    def __init__(self, controller, dashboard_view=None, user_controller=None, parent=None, type =None):
        super().__init__()
        self.controller = controller
        self.dashboard_view = dashboard_view
        self.user_controller = user_controller
        self.type = type
        self.setWindowTitle('ContractView')
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        if parent:
            self.setGeometry(parent.geometry())

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
                           
            QPushButton#dashboard_button {
                background-color: black;
                max-width: 200px;
                min-height: 50px;
                font-size: 20px;
            }

            QFrame#contract_frame {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 10px;
            }

            QWidget#contract_widget {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
                min-height: 500px;
            }

            QPushButton#elimina_contratto_button {
                background-color: #e74c3c;
            }
            QPushButton#elimina_contratto_button:hover {
                background-color: #c0392b;
            }

            QPushButton#view_fatture_button {
                background-color: #2980b9;
            }
            QPushButton#view_fatture_button:hover {
                background-color: #1f6391;
            }
            QPushButton#crea_contratto_acquisto_button{
                background-color: black;
                min-height: 40px;
                font-size: 20px;
            }
            QPushButton#crea_contratto_noleggio_button{
                background-color: black;
                min-height: 40px;    
                font-size: 20px;
            }          
        """)

        self.populateContracts()
        self.centerWindow(self)

    def populateContracts(self):
        # Rimuovi tutti i widget dal layout principale
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        button_layout = QHBoxLayout()
        dashboard_btn = QPushButton('Torna alla Dashboard')
        dashboard_btn.setObjectName('dashboard_button')
        dashboard_btn.clicked.connect(self.goToDashboard)
        button_layout.addWidget(dashboard_btn)
        button_layout.addStretch()
        self.main_layout.addLayout(button_layout)

        contract_frame = QFrame()
        contract_frame.setObjectName('contract_frame')
        contract_grid_layout = QGridLayout(contract_frame)
        self.controller.contract_model.loadContracts()  # ricarica i dati da file
        role = self.user_controller.getRuoloUtente()
        if role == 'amministratore':
            contracts = self.controller.getContratti()
        else:
            contracts = self.controller.getContrattiCliente(self.user_controller.getDatiUtenteLoggato().get('username'))

        rent_contracts = [c for c in contracts if c.get('tipo') == 'noleggio']
        buy_contracts = [c for c in contracts if c.get('tipo') == 'acquisto']
        
        #print("contratti totali: ")
        #for c in contracts:
            #print(c)
        #print("contratti acquisto: ")
        #for c in buy_contracts:
            #print(c)
        #print("contratti noleggio: ")
        #for c in rent_contracts:
            #print(c)
        

        
        auto_list = GestoreAuto(self.user_controller).getAllAuto()
        if not auto_list:        
            auto_list = []
        if self.type != 'acquisto':
            for i, contract in enumerate(rent_contracts):

                contract_widget = QWidget()
                contract_widget.setObjectName('contract_widget')
                contract_layout = QVBoxLayout(contract_widget)
                contract_layout.setContentsMargins(10, 10, 10, 10)

                user_label = QLabel(f"Utente: {contract['user']}")
                user_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)



                auto_label = QLabel("Auto: non trovata")
                auto_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                for auto in auto_list:
                    #print(f"{auto}")
                    if auto['id'] == contract['auto']:
                        print(f"trovato auto per contratto {contract['id']}: {auto}")
                        auto_label.setText(f"Auto: {auto['marca']} {auto['modello']} {auto['targa']}")
                        auto_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                start_date_label = QLabel(f"Data inizio: {contract['start_date']}")
                start_date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                end_date_label = QLabel(f"Data fine: {contract['end_date']}")
                end_date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                cauzione_label = QLabel(f"Cauzione: {contract['cauzione']}€")
                cauzione_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                price_label = QLabel(f"Prezzo: {contract['prezzoTot']}€")
                price_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                tipoGaranzia_label = QLabel(f"Tipo garanzia: {contract['tipoGaranzia']}")
                tipoGaranzia_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                durataGaranzia_label = QLabel(f"Durata garanzia: {contract['durataGaranzia']} mesi")
                durataGaranzia_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                kmMax_label = QLabel(f"Chilometri massimi: {contract['kmMax']}")
                kmMax_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


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
                view_fatture_btn.clicked.connect(lambda checked, c=contract: self.showFattureView(c))
                contract_layout.addWidget(view_fatture_btn)

                if role == 'amministratore':
                    elimina_contract_btn = QPushButton('Elimina contratto')
                    elimina_contract_btn.setObjectName('elimina_contratto_button')
                    elimina_contract_btn.clicked.connect(
                        lambda checked=False, c=contract: self.controller.eliminaContrattieFatture(c['id'], c['auto'], self))
                    contract_layout.addWidget(elimina_contract_btn)

                contract_grid_layout.addWidget(contract_widget, i // 4, i % 4)


        if self.type != 'noleggio':
            for i, contract in enumerate(buy_contracts):
                contract_widget = QWidget()
                contract_widget.setObjectName('contract_widget')
                contract_layout = QVBoxLayout(contract_widget)
                contract_layout.setContentsMargins(10, 10, 10, 10)

                user_label = QLabel(f"Utente: {contract['user']}")
                user_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                
                auto_label.setText(f"Auto: {contract['auto']}")
                auto_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                price_label = QLabel(f"Prezzo: {contract['price']}€")
                price_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                tipoGaranzia_label = QLabel(f"Tipo garanzia: {contract['tipoGaranzia']}")
                tipoGaranzia_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                durataGaranzia_label = QLabel(f"Durata garanzia: {contract['durataGaranzia']} mesi")
                durataGaranzia_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


                contract_layout.addWidget(user_label)
                contract_layout.addWidget(auto_label)
                contract_layout.addWidget(price_label)
                contract_layout.addWidget(tipoGaranzia_label)
                contract_layout.addWidget(durataGaranzia_label)

                if role == 'amministratore':
                    elimina_contract_btn = QPushButton('Elimina contratto')
                    elimina_contract_btn.setObjectName('elimina_contratto_button')
                    elimina_contract_btn.clicked.connect(
                        lambda checked=False, c=contract: self.controller.eliminaContrattieFatture(c['id'], c['auto'], self))
                    contract_layout.addWidget(elimina_contract_btn)

                contract_grid_layout.addWidget(contract_widget, (i + len(rent_contracts)) // 4, (i + len(rent_contracts)) % 4)

            
            
            
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(contract_frame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # disabilita lo scroll orizzontale
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.main_layout.addWidget(scroll_area)
        #self.main_layout.addStretch()
        
        if role == 'amministratore':
            admin_buttons_layout = QHBoxLayout()
            crea_acquisto_contract_btn = QPushButton('Crea contratto acquisto')
            crea_acquisto_contract_btn.setObjectName('crea_contratto_acquisto_button')
            crea_acquisto_contract_btn.clicked.connect(self.controller.creaContrattoAcquistoDialog)
            admin_buttons_layout.addWidget(crea_acquisto_contract_btn)

            crea_noleggio_contract_btn = QPushButton('Crea contratto noleggio')
            crea_noleggio_contract_btn.setObjectName('crea_contratto_noleggio_button')
            crea_noleggio_contract_btn.clicked.connect(self.controller.creaContrattoNoleggioDialog)
            admin_buttons_layout.addWidget(crea_noleggio_contract_btn)

            self.main_layout.addLayout(admin_buttons_layout)

        





###---FUNZIONI---###--------------------------------------------



    def showFattureView(self, contract):
        role = self.user_controller.getRuoloUtente()
        self.fatture_view = FattureView(self.controller, contract, role, parent=self)
        self.controller.fatture_view = self.fatture_view
        self.fatture_view.setWindowTitle(f"Fatture per il contratto: {contract['id']}")
        self.fatture_view.show()

    def refreshContracts(self):
        self.populateContracts()

    def goToDashboard(self):
        self.hide()
        self.dashboard_view.show()

    def centerWindow(self, view):
            """Centra la finestra sullo schermo"""
            screen = view.screen().availableGeometry()
            view.move(
                max(0, (screen.width() - view.width()) // 2),
                max(0, (screen.height() - view.height()) // 2)
            )
    