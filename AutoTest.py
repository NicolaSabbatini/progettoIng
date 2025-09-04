import unittest
from unittest.mock import patch
from controllers.GestoreAuto import GestoreAuto
from models.Auto import Auto

class DummyView:
    def refresh_auto(self):
        self.refreshed = True

class TestGestoreAutoModifica(unittest.TestCase):
    def setUp(self):
        patcher_save = patch.object(Auto, 'save_auto', return_value=None)
        patcher_load = patch.object(Auto, 'load_auto', return_value=[])
        self.mock_save = patcher_save.start()
        self.mock_load = patcher_load.start()
        self.addCleanup(patcher_save.stop)
        self.addCleanup(patcher_load.stop)

        self.auto_model = Auto()
        self.auto_model.auto_list = []
        self.user_controller = None
        self.gestore = GestoreAuto(self.user_controller)
        self.gestore.auto_model.auto_list = [{
            'id': 1,
            'marca': 'Fiat',
            'modello': 'Panda',
            'anno': '2020',
            'chilometri': '10000',
            'prezzo': '9000',
            'targa': 'AB123CD',
            'visibile': True
        }]
        self.auto_id = 1

    def test_modifica_auto_success(self):
        success, msg = self.gestore.salvaModificaAuto(
            self.auto_id, 'Fiat', 'Punto', '2021', '12000', '9500', 'AB123CD'
        )
        self.assertTrue(success)
        self.assertIn("modificata", msg)
        auto = self.gestore.get_all_auto()[0]
        self.assertEqual(auto['modello'], 'Punto')
        self.assertEqual(auto['anno'], '2021')
        self.assertEqual(auto['chilometri'], '12000')
        self.assertEqual(auto['prezzo'], '9500')

    def test_modifica_auto_missing_id(self):
        success, msg = self.gestore.salvaModificaAuto(
            None, 'Fiat', 'Punto', '2021', '12000', '9500', 'AB123CD'
        )
        self.assertFalse(success)
        self.assertIn("ID dell'auto non valido", msg)

    def test_modifica_auto_not_found(self):
        success, msg = self.gestore.salvaModificaAuto(
            9999, 'Fiat', 'Punto', '2021', '12000', '9500', 'AB123CD'
        )
        self.assertFalse(success)
        self.assertIn("auto non trovata", msg.lower())

if __name__ == '__main__':
    unittest.main()