import unittest
from unittest.mock import patch
from controllers.GestoreUtenti import GestoreUtenti
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys


app = QApplication(sys.argv)

class DummyView:
    def hide(self): pass
    def show(self): pass
    def clear_fields(self): pass

class TestGestoreUtenti(unittest.TestCase):
    def setUp(self):
        self.login_view = DummyView()
        self.register_view = DummyView()
        self.dashboard_view = DummyView()
        self.gestore = GestoreUtenti(
            login_view=self.login_view,
            register_view=self.register_view,
            dashboard_view=self.dashboard_view
        )

    def test_login_missing_fields(self):
        success = self.gestore.login('', '', None)
        self.assertFalse(success) 
 
    def test_login_wrong_credentials(self):
        success = self.gestore.login('utente_non_esistente', 'password_sbagliata', None)
        self.assertFalse(success)

    def test_register_missing_fields(self):
        success, msg = self.gestore.register('', '', '', '', '', '', '', '', '')
        self.assertFalse(success)
        self.assertIn("obbligatori", msg)

    def test_register_password_mismatch(self):
        success, msg = self.gestore.register('user', 'mail@mail.com', 'pass1', 'pass2', 'nome', 'cognome', 'luogo', 'tel', '2000-01-01')
        self.assertFalse(success)
        self.assertIn("non coincidono", msg)

    def test_register_short_password(self):
        success, msg = self.gestore.register('user', 'mail@mail.com', '123', '123', 'nome', 'cognome', 'luogo', 'tel', '2000-01-01')
        self.assertFalse(success)
        self.assertIn("almeno 6 caratteri", msg)

    def test_register_invalid_email(self):
        success, msg = self.gestore.register('user', 'mailmailcom', 'password', 'password', 'nome', 'cognome', 'luogo', 'tel', '2000-01-01')
        self.assertFalse(success)
        self.assertIn("Formato email non valido", msg)

if __name__ == '__main__':
    unittest.main()