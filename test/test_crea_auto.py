import unittest
from unittest.mock import MagicMock
from controllers.auto_controller import CreaAutoDialog, AutoController
from PyQt5.QtWidgets import QApplication, QLineEdit

app = QApplication([])  # Serve per testare QWidget

class TestCreaAutoDialog(unittest.TestCase):
    def setUp(self):
        self.controller = AutoController()
        self.controller.addo_auto = MagicMock(return_value=(True, "Auto aggiunta con successo"))
        self.dialog = CreaAutoDialog(controller=self.controller)

    def test_addi_auto_success(self):
        # Compila i campi
        self.dialog.marca_input.setText("Fiat")
        self.dialog.modello_input.setText("Panda")
        self.dialog.anno_input.setText("2020")
        self.dialog.chilometri_input.setText("5000")
        self.dialog.prezzo_input.setText("10000")
        self.dialog.targa_input.setText("AB123CD")

        self.dialog.addi_auto()

        self.controller.addo_auto.assert_called_once_with(
            "Fiat", "Panda", "2020", "5000", "10000", "AB123CD"
        )

    def test_addi_auto_fail_empty_fields(self):
        # Lascia i campi vuoti
        self.dialog.marca_input.setText("")
        self.dialog.modello_input.setText("")
        
        # Non lancerà eccezione, ma deve chiamare QMessageBox
        with unittest.mock.patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_msg:
            self.dialog.addi_auto()
            mock_msg.assert_called_once()

if __name__ == "__main__":
    unittest.main()
