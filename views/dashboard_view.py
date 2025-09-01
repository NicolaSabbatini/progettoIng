from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QGridLayout, QLineEdit, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

from models.auto_model import AutoModel
from models.contract_model import ContractModel
from controllers.GestoreContratti import GestoreContratti
from controllers.GestoreAuto import GestoreAuto
from views.contract_view import ContractView
from views.auto_view import AutoView


class DashboardView(QWidget):
    def __init__(self, controller, login_view=None, auth_controller=None):
        super().__init__()
        self.controller = controller
        self.login_view = login_view
        self.auth_controller = auth_controller
        #self.auto_model = AutoModel()
        #self.controller.set_dashboard_view(self)  # 👈 collega la view al controller
        #self.contract_model = ContractModel()
        self.resize(700, 550)  # dimensione iniziale
        self.setWindowTitle('Dashboard')

        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Dashboard')
        self.resize(700,550)
        #self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b; /* grigio scuro */
                color: white; /* testo bianco */
            }

            QLabel {
                color: white;
                font-size: 22px;
            }

            QPushButton {
                background-color: black;
                color: white;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 6px 12px;
                min-width: 180px;
                max-width: 450px;
                min-height: 40px;
                font-size: 18px;
            }

            QPushButton:hover {
                background-color: #444;
            }

            QLineEdit, QTextEdit {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 4px;
            }

            QFrame#info_frame {
                background-color: #1e1e1e;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 10px;
            }

            QLabel#section_title {
                font-size: 24px;
                font-weight: bold;
                color: #f39c12; /* giallo/arancio per i titoli */
            }

            QPushButton#logout_button {
                background-color: #e74c3c;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 16px;
                max-width: 80px;
            }
            QPushButton#logout_button:hover {
                background-color: #c0392b;
            }
        """)
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel('Benvenuto/a!')
        self.welcome_label.setObjectName('welcome_title')
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        
        self.logout_button = QPushButton('Logout')
        self.logout_button.setObjectName('logout_button')
        self.logout_button.clicked.connect(self.controller.handle_logout)
        header_layout.addWidget(self.logout_button)
        
        main_layout.addLayout(header_layout)
        
        # Frame informazioni utente
        info_frame = QFrame()
        info_frame.setObjectName('info_frame')
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(25)
        
        info_title = QLabel('Informazioni Account')
        info_title.setObjectName('section_title')
        info_layout.addWidget(info_title)
        
        # Campi informazioni
        self.username_label = QLabel()
        self.email_label = QLabel()
        self.created_label = QLabel()
        self.login_time_label = QLabel()
        self.username_label.setObjectName('info_label')
        self.email_label.setObjectName('info_label')
        self.created_label.setObjectName('info_label')
        self.login_time_label.setObjectName('info_label')
        self.name_label = QLabel()
        self.name_label.setObjectName('info_label')
        self.surname_label = QLabel()
        self.surname_label.setObjectName('info_label')
        self.luogo_label = QLabel()
        self.luogo_label.setObjectName('info_label')
        self.telefono_label = QLabel()
        self.telefono_label.setObjectName('info_label')
        self.data_label = QLabel()
        self.data_label.setObjectName('info_label')
        self.controller.update_user_info(self)
       
        
        info_layout.addWidget(self.username_label)
        info_layout.addWidget(self.email_label)
        info_layout.addWidget(self.created_label)
        info_layout.addWidget(self.login_time_label)
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.surname_label)
        info_layout.addWidget(self.luogo_label)
        info_layout.addWidget(self.telefono_label)
        info_layout.addWidget(self.data_label)
        info_layout.addStretch()

        
        main_layout.addWidget(info_frame)

        role = self.controller.get_current_user_role()
        if role == 'amministratore':
            contratti_scaduti_frame = QFrame()
            contratti_scaduti_frame.setObjectName('contratti_scaduti_frame')
            contratti_scaduti_layout = QVBoxLayout(contratti_scaduti_frame)
            contratti_scaduti_layout.setSpacing(25)


            self.notification_label = QLabel()
            self.notification_label.setStyleSheet("color: #e74c3c; font-size: 16px;")
            self.notification_label.hide()
            contratti_scaduti_layout.addWidget(self.notification_label)

            main_layout.addWidget(contratti_scaduti_frame)
            

            

        main_layout.addStretch()
        buttons_layout = QHBoxLayout()
        
        
        show_contract_btn = QPushButton('visualizza contratti clienti')
        show_contract_btn.setObjectName('show_contract_button')
        show_contract_btn.clicked.connect(self.show_contract)
        buttons_layout.addWidget(show_contract_btn)

        
        if role == 'cliente':
            show_contract_btn = QPushButton('visualizza contratti')
            show_contract_btn.setObjectName('show_contract_button')
            show_contract_btn.clicked.connect(self.show_contract_client)
            buttons_layout.addWidget(show_contract_btn)


        show_auto_btn = QPushButton('Visualizza Auto')
        show_auto_btn.setObjectName('show_auto_button')
        show_auto_btn.clicked.connect(self.show_auto)
        buttons_layout.addWidget(show_auto_btn)
                

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)
        
        # Centra la finestra
        self.center_window(self)

        self.verificaScadenzaNoleggio()




    
    ###---FUNZIONI---###--------------------------------------------

    def verificaScadenzaNoleggio(self):
        contract_controller = GestoreContratti(self.controller, self)
        contract_controller.check_contracts_and_notify_dashboard(self)
        
    def show_notification(self, message):
        if hasattr(self, 'notification_label'):
            self.notification_label.setText(message)
            self.notification_label.show()

    

   
   
    def show_contract(self):
        # creo il controller (gli passo anche la dashboard, così ci torna indietro)
        contract_controller = GestoreContratti(self.controller, dashboard_view=self)
        
        # creo la contract view e la collego al controller
        contract_view = ContractView(contract_controller, dashboard_view=self, user_controller = self.controller, parent=self)
        contract_controller.contract_view = contract_view  
        
        # mostro la contract view e nascondo la dashboard
        contract_view.show()
        self.hide()
   
    def show_contract_client(self):
        contract_controller = GestoreContratti(self.controller, dashboard_view=self)
        # creo la contract view e la collego al controller
        contract_view = ContractView(contract_controller, dashboard_view=self, user_controller = self.controller, parent=self)
        contract_controller.contract_view = contract_view  
        # mostro la contract view e nascondo la dashboard
        contract_view.show()
        self.hide()






    def show_auto(self):
        # creo il controller (gli passo anche la dashboard, così ci torna indietro)
        auto_controller = GestoreAuto(self.controller, dashboard_view=self)
        # creo la auto view e la collego al controller
        auto_view = AutoView(auto_controller, user_controller=self.controller, dashboard_view=self, parent=self)
        auto_controller.auto_view = auto_view  
        # mostro la auto view e nascondo la dashboard
        auto_view.show()
        self.hide()


    
    
    
    
    
    def center_window(self, view):
            """Centra la finestra sullo schermo"""
            screen = view.screen().availableGeometry()
            size = view.geometry()
            view.move(
                max(0, (screen.width() - view.width()) // 2),
                max(0, (screen.height() - view.height()) // 2)
            )




 