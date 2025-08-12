from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QGridLayout, QLineEdit, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

from models.auto import AutoModel
from models.contract_model import ContractModel
from controllers.auth_controller import AuthController

class DashboardView(QWidget):
    def __init__(self, controller, login_view):
        super().__init__()
        self.controller = controller
        self.login_view = login_view
        self.auto_model = AutoModel()
        self.contract_model = ContractModel()
        self.setWindowTitle('Dashboard')


        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Dashboard')
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
        self.logout_button.clicked.connect(self.handle_logout)
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
        self.update_user_info()
       
        
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
    
            auto_layout.addWidget(marca_label)
            auto_layout.addWidget(modello_label)
            auto_layout.addWidget(anno_label)
    

            grid_auto_layout.addWidget(auto_widget, i // 4, i % 4)


        

        crea_auto_btn = QPushButton('Crea Auto')
        crea_auto_btn.setObjectName('crea_auto_button')
        crea_auto_btn.clicked.connect(self.crea_auto)
        
        show_contract_btn = QPushButton('visualizza contratti')
        show_contract_btn.setObjectName('show_contract_button')
        show_contract_btn.clicked.connect(self.visualizza_contratti)

        crea_contract_btn = QPushButton('crea contratto')
        crea_contract_btn.setObjectName('crea_contratto_button')
        crea_contract_btn.clicked.connect(self.crea_contratto)


        main_layout.addWidget(auto_frame)
        main_layout.addWidget(crea_auto_btn)
        main_layout.addWidget(show_contract_btn)
        main_layout.addWidget(auto_frame)
        main_layout.addWidget(crea_contract_btn)



        main_layout.addStretch()
        


        self.setLayout(main_layout)
        
        # Centra la finestra
        self.center_window()
    
    
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            max(0, (screen.width() - self.width()) // 2),
            max(0, (screen.height() - self.height()) // 2)
        )
    
    def update_user_info(self):
        """Aggiorna le informazioni utente nella dashboard"""
        user_data = self.controller.get_current_user_data()
        
        if user_data:
            self.welcome_label.setText(f'Benvenuto, {user_data["username"]}!')
            self.username_label.setText(f'👤 Username: {user_data["username"]}')
            self.email_label.setText(f'📧 Email: {user_data["email"]}')
            self.created_label.setText(f'📅 Account creato: {user_data["created_at"]}')
            self.login_time_label.setText(f'🕐 Ultimo accesso: {user_data["login_time"]}')
            self.name_label.setText(f'Nome: {user_data.get("name", "N/A")}')
            self.surname_label.setText(f'Cognome: {user_data.get("surname", "N/A")}')
            self.luogo_label.setText(f'Luogo: {user_data.get("luogo", "N/A")}')
            self.telefono_label.setText(f'Telefono: {user_data.get("telefono", "N/A")}')
            self.data_label.setText(f'Data di nascita: {user_data.get("data", "N/A")}')

    
    def handle_logout(self):
        """Gestisce il logout"""
        self.controller.logout()
        self.login_view.clear_fields()
        self.login_view.show()
        self.hide()


    def update_auto_display(self):
        """Aggiorna la visualizzazione delle auto nella dashboard"""
        auto_list = self.controller.get_all_auto()
        
        if not hasattr(self, 'auto_layout'):
            self.auto_layout = QGridLayout()
            self.auto_layout.setSpacing(10)
            self.auto_layout.setContentsMargins(0, 0, 0, 0)
            self.auto_frame = QFrame()
            self.auto_frame.setObjectName('info_frame')
            self.auto_frame.setLayout(self.auto_layout)
            self.layout().addWidget(self.auto_frame)
        
        # Pulisce il layout esistente
        for i in reversed(range(self.auto_layout.count())): 
            widget = self.auto_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Crea e aggiunge i widget per le auto
        if auto_list:
            self.create_auto_widgets(auto_list)



    def crea_auto(self):
        dialog = CreaAutoDialog(self.controller, self)
        dialog.exec_()

    def crea_contratto(self):
        dialog = CreaContract(self, self.controller)
        dialog.exec_()

    
    def visualizza_contratti(self):
        """Visualizza i contratti associati all'utente"""
        contracts = self.controller.get_all_contracts()
        if not contracts:
            QMessageBox.information(self, 'Contratti', 'Nessun contratto trovato.')
            return
            
        contract_frame = QFrame()
        contract_frame.setObjectName('contract_frame')
        contract_grid_layout = QGridLayout(contract_frame)

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


        

            contract_grid_layout.addWidget(contract_widget, i // 4, i % 4)

            self.layout().addWidget(contract_frame)

class CreaContract(QDialog):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle('Crea un nuovo contratto')
        self.setFixedSize(350,250)
        layout = QVBoxLayout(self)

        user_input = QLineEdit()
        user_input.setPlaceholderText('user')
        layout.addWidget(QLabel('user:'))
        layout.addWidget(user_input)

        auto_input = QLineEdit()
        auto_input.setPlaceholderText('auto')
        layout.addWidget(QLabel('auto:'))
        layout.addWidget(auto_input)

        start_date_input = QLineEdit()
        start_date_input.setPlaceholderText('start_date')
        layout.addWidget(QLabel('start date:'))
        layout.addWidget(start_date_input)

        end_date_input = QLineEdit()
        end_date_input.setPlaceholderText('end_date')
        layout.addWidget(QLabel('end date:'))
        layout.addWidget(end_date_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo:'))
        layout.addWidget(prezzo_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva contratto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_contract(user_input,auto_input,start_date_input,end_date_input,prezzo_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_contract(self, user_input, auto_input, start_date_input, end_date_input, prezzo_input):
        user = user_input.text()
        auto = auto_input.text()
        start_date = start_date_input.text()
        end_date = end_date_input.text()
        prezzo = prezzo_input.text()


        if user and auto and start_date and end_date and prezzo:
            self.controller.addo_contratto(user,auto,start_date,end_date,prezzo)
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')

    
class CreaAutoDialog(QDialog):
    def __init__(self,controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle('Crea una Nuova Auto')
        self.setFixedSize(350, 250)
        layout = QVBoxLayout(self)

        marca_input = QLineEdit()
        marca_input.setPlaceholderText('Marca')
        layout.addWidget(QLabel('Marca:'))
        layout.addWidget(marca_input)

        modello_input = QLineEdit()
        modello_input.setPlaceholderText('Modello')
        layout.addWidget(QLabel('Modello:'))
        layout.addWidget(modello_input)

        anno_input = QLineEdit()
        anno_input.setPlaceholderText('Anno')
        layout.addWidget(QLabel('Anno:'))
        layout.addWidget(anno_input)
        
      
        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva Auto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_auto(marca_input, modello_input, anno_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)





    def addi_auto(self, marca_input, modello_input, anno_input):
        marca = marca_input.text()
        modello = modello_input.text()
        anno = anno_input.text()

        if marca and modello and anno:
            self.controller.addo_auto(marca, modello, anno)
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')

