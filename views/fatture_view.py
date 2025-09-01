from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout, QPushButton

class FattureView(QWidget):
    def __init__(self, controller, contract, role = 'cliente', parent =None):
        super().__init__()
        self.controller = controller
        self.contract = contract
        self.role = role
        self.setWindowTitle('Fatture per il Contratto')
        if parent:
            self.setGeometry(parent.geometry())

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)

        self.populate_fatture()
        self.center_window()

    def populate_fatture(self):
        # Remove previous fatture frame if exists
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QFrame) or isinstance(widget, QPushButton):
                self.main_layout.removeWidget(widget)
                widget.deleteLater()

        fatture_frame = QFrame()
        fatture_frame.setObjectName('fatture_frame')
        grid_fatture_layout = QGridLayout(fatture_frame)

        fatture_list = self.controller.get_fatture_by_contratto(self.contract['id'])
        for i, fattura in enumerate(fatture_list):
            fatture_widget = QWidget()
            fatture_widget.setObjectName('fatture_widget')
            fatture_layout = QVBoxLayout(fatture_widget)
            fatture_layout.setContentsMargins(10, 10, 10, 10)

            id_label = QLabel(f"ID Fattura: {fattura['idfattura']}")
            contratto_label = QLabel(f"Contratto: {fattura['contratto']}")
            data_label = QLabel(f"Data: {fattura['data']}")
            prezzo_label = QLabel(f"Prezzo: {fattura['prezzo']}")

            fatture_layout.addWidget(id_label)
            fatture_layout.addWidget(contratto_label)
            fatture_layout.addWidget(data_label)
            fatture_layout.addWidget(prezzo_label)

            grid_fatture_layout.addWidget(fatture_widget, i // 4, i % 4)

        self.main_layout.addWidget(fatture_frame)
        if self.role == 'amministratore':
            crea_fattura_button = QPushButton('Crea Fattura')
            crea_fattura_button.setObjectName('crea_fattura_button')
            crea_fattura_button.clicked.connect(self.create_fattura)
            self.main_layout.addWidget(crea_fattura_button)
        self.main_layout.addStretch()

    def create_fattura(self):
        # Call the controller to create a fattura, then refresh the view
        self.controller.create_fattura_button(self.contract['id'])
        self.populate_fatture()

    def center_window(self):
        screen = self.screen().availableGeometry()
        self.move(
            max(0, (screen.width() - self.width()) // 2),
            max(0, (screen.height() - self.height()) // 2)
        )

    def refresh_fatture(self):
        self.populate_fatture()