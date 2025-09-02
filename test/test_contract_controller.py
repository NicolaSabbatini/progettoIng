import unittest
from unittest.mock import MagicMock
from controllers.GestoreContratti import GestoreContratti

class TestContractController(unittest.TestCase):
    def setUp(self):
        self.controller = GestoreContratti(main_controller=MagicMock())
        # Mock dei modelli
        self.controller.contract_model = MagicMock()
        self.controller.buy_contract_model = MagicMock()
        self.controller.rent_contract_model = MagicMock()
        self.controller.fatture_model = MagicMock()
        # Mock della view
        self.controller.contract_view = MagicMock()
    
    def test_addo_noleggio_contratto_success(self):
        success, message = self.controller.addo_noleggio_contratto(
            "user1", "auto1", "2025-01-01", "2025-01-10", 500, "garanzia1", "12 mesi", 1000, 1000
        )
        self.assertTrue(success)
        self.assertEqual(message, "Contratto aggiunto con successo")
        self.controller.rent_contract_model.add_rent_contract.assert_called_once()
    
    def test_addo_noleggio_contratto_fail_missing_fields(self):
        success, message = self.controller.addo_noleggio_contratto(
            "", "", "", "", "", "", "", "", ""
        )
        self.assertFalse(success)
        self.assertEqual(message, "Tutti i campi del contratto sono obbligatori")
    
    def test_addo_acquisto_contratto_success(self):
        success, message = self.controller.addo_acquisto_contratto(
            "user1", "auto1", "garanzia1", "12 mesi", 1000
        )
        self.assertTrue(success)
        self.assertEqual(message, "Contratto aggiunto con successo")
        self.controller.buy_contract_model.add_buy_contract.assert_called_once()
    
    def test_addo_acquisto_contratto_fail_missing_fields(self):
        success, message = self.controller.addo_acquisto_contratto("", "", "", "", "")
        self.assertFalse(success)
        self.assertEqual(message, "Tutti i campi del contratto sono obbligatori")
    

if __name__ == "__main__":
    unittest.main()
