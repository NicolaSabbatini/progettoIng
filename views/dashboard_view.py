from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QGridLayout, QLineEdit, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

from models.auto_model import AutoModel
from models.contract_model import ContractModel
from controllers.contract_controller import ContractController
from controllers.auto_controller import AutoController
from views.contract_view import ContractView
from views.auto_view import AutoView


class DashboardView(QWidget):
    def __init__(self, controller, login_view=None):
        super().__init__()
        self.controller = controller
        self.login_view = login_view
        self.auto_model = AutoModel()
        #self.contract_model = ContractModel()
        self.setWindowTitle('Dashboard')


        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Dashboard')
        self.setFixedSize(700,550)
        #self.setFixedSize(600, 400)
        
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QHBoxLayout()
        self.welcome_label = QLabel('Benvenuto!')
        self.welcome_label.setObjectName('welcome_title')
        header_layout.addWidget(self.welcome_label)
        header_layout.addStretch()
        
        self.logout_button = QPushButton('Logout')
        self.logout_button.setObjectName('logout_button')
        self.logout_button.clicked.connect(lambda: self.controller.handle_logout(self))
        header_layout.addWidget(self.logout_button)
        
        main_layout.addLayout(header_layout)
        
        # Frame informazioni utente
        info_frame = QFrame()
        info_frame.setObjectName('info_frame')
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
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
        

    
        


        

        
        show_contract_btn = QPushButton('visualizza contratti')
        show_contract_btn.setObjectName('show_contract_button')
        show_contract_btn.clicked.connect(self.show_contract)



        show_auto_btn = QPushButton('Visualizza Auto')
        show_auto_btn.setObjectName('show_auto_button')
        show_auto_btn.clicked.connect(self.show_auto)


        main_layout.addWidget(show_contract_btn)
        main_layout.addWidget(show_auto_btn)



        main_layout.addStretch()
        


        self.setLayout(main_layout)
        
        # Centra la finestra
        self.controller.center_window(self)

    def show_contract(self):
    # creo il controller (gli passo anche la dashboard, così ci torna indietro)
        contract_controller = ContractController(self.controller, dashboard_view=self)

        # creo la contract view e la collego al controller
        contract_view = ContractView(contract_controller, dashboard_view=self)
        contract_controller.contract_view = contract_view  

        # mostro la contract view e nascondo la dashboard
        contract_view.show()
        self.hide()

    def show_auto(self):
        # creo il controller (gli passo anche la dashboard, così ci torna indietro)
        auto_controller = AutoController(self.controller, dashboard_view=self)

        # creo la auto view e la collego al controller
        auto_view = AutoView(auto_controller, dashboard_view=self)
        auto_controller.auto_view = auto_view  

        # mostro la auto view e nascondo la dashboard
        auto_view.show()
        self.hide()

