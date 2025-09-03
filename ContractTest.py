import unittest
from controllers.GestoreContratti import GestoreContratti

class DummyView:
    def refresh_contracts(self):
        self.refreshed = True

class TestGestoreContrattiCreazione(unittest.TestCase):
    def setUp(self):
        self.contract_view = DummyView()
        self.gestore = GestoreContratti(contract_view=self.contract_view)

    def test_crea_noleggio_contratto_missing_fields(self):
        # Tutti i campi vuoti
        success, msg = self.gestore.addo_noleggio_contratto('', '', '', '', '', '', '', '', '')
        self.assertFalse(success)
        self.assertIn("obbligatori", msg)

    def test_crea_acquisto_contratto_missing_fields(self):
        # Tutti i campi vuoti
        success, msg = self.gestore.addo_acquisto_contratto('', '', '', '', '')
        self.assertFalse(success)
        self.assertIn("obbligatori", msg)