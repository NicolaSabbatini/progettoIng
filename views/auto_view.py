from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class AutoView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Auto")

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Marca")

        self.modello_input = QLineEdit()
        self.modello_input.setPlaceholderText("Modello")

        self.anno_input = QLineEdit()
        self.anno_input.setPlaceholderText("Anno")

        self.salva_btn = QPushButton("Salva Auto")
        self.output_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.marca_input)
        layout.addWidget(self.modello_input)
        layout.addWidget(self.anno_input)
        layout.addWidget(self.salva_btn)
        layout.addWidget(self.output_label)

        self.setLayout(layout)