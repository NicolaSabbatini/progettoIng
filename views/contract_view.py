from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QGridLayout, QLineEdit, QDialog, QMessageBox)
from PyQt5.QtCore import Qt

from models.auto_model import AutoModel
from models.contract_model import ContractModel


class ContractView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('ContractView')
        self.init_ui()

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


        

            contract_grid_layout.addWidget(contract_widget, i // 4, i % 4)

            self.layout().addWidget(contract_frame)

