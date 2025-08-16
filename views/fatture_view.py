from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QFrame, QGridLayout, QWidget


class FattureView(QWidget):
    def __init__(self, controller, contract):
        super().__init__()
        self.controller = controller
        self.contract = contract
        self.setWindowTitle('Fatture per il Contratto')

        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Dashboard')
        #self.setFixedSize(600, 400)
        
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)


        fatture_frame = QFrame()
        fatture_frame.setObjectName('fatture_frame')
        grid_fatture_layout = QGridLayout(fatture_frame)

        for i, fattura in enumerate(self.controller.get_fatture_by_contratto(self.contract['id'])):
            fatture_widget = QWidget()
            fatture_widget.setObjectName('fatture_widget')
            fatture_layout = QVBoxLayout(fatture_widget)
            fatture_layout.setContentsMargins(10, 10, 10, 10)
    
            id_label = QLabel(f"Marca: {fattura['id']}")
            contratto_label = QLabel(f"Modello: {fattura['contratto']}")
            data_label = QLabel(f"Anno: {fattura['data']}")
    
            fatture_layout.addWidget(id_label)
            fatture_layout.addWidget(contratto_label)
            fatture_layout.addWidget(data_label)
    

            grid_fatture_layout.addWidget(fatture_widget, i // 4, i % 4)










        #layout.addWidget(QLabel(f"Contratto: {contract['user']} - {contract['auto']}"))

        # Example: Load fatture from contract['fatture'] or from a model
        #fatture_list = self.controller

        #list_widget = QListWidget()
        #for fattura in fatture_list:
            #list_widget.addItem(f"Fattura ID: {fattura['id']} - Importo: {fattura['importo']} - Data: {fattura['data']}")
        #layout.addWidget(list_widget)