from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget

class FattureView(QDialog):
    def __init__(self, contract, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Fatture per Contratto ID {contract['id']}")
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Contratto: {contract['user']} - {contract['auto']}"))

        # Example: Load fatture from contract['fatture'] or from a model
        fatture_list = contract.get('fatture', [])  # Or fetch from a model

        list_widget = QListWidget()
        for fattura in fatture_list:
            list_widget.addItem(f"Fattura ID: {fattura['id']} - Importo: {fattura['importo']} - Data: {fattura['data']}")
        layout.addWidget(list_widget)