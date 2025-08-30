import unittest
from unittest.mock import MagicMock
from controllers.contract_controller import CreaRentContract, ContractController

class TestCreaRentContract(unittest.TestCase):
    def setUp(self):
        # Mock del controller
        self.mock_controller = MagicMock(spec=ContractController)
        # Mock della view
        self.mock_contract_view = MagicMock()
        # Istanza del dialog
        self.dialog = CreaRentContract(
            parent=None,
            controller=self.mock_controller,
            contract_view=self.mock_contract_view
        )

        # Creiamo QLineEdit simulati usando MagicMock
        self.mock_inputs = {}
        for field in [
            "user", "auto", "start_date", "end_date",
            "cauzione", "prezzo", "durataGaranzia",
            "tipoGaranzia", "kmMax"
        ]:
            mock_input = MagicMock()
            mock_input.text.return_value = field + "_value"
            self.mock_inputs[field] = mock_input

    def test_addi_contract_various_cases(self):
        # Definiamo scenari diversi: tutti i campi, mancanza di uno, mancanza di due
        scenarios = [
            ("all_fields", {k: v.text.return_value for k, v in self.mock_inputs.items()}, True),
            ("missing_user", {**{k: v.text.return_value for k, v in self.mock_inputs.items()}, "user": ""}, False),
            ("missing_auto", {**{k: v.text.return_value for k, v in self.mock_inputs.items()}, "auto": ""}, False),
            ("missing_multiple", {**{k: v.text.return_value for k, v in self.mock_inputs.items()}, "user": "", "auto": ""}, False)
        ]

        for name, input_values, should_call in scenarios:
            with self.subTest(name=name):
                # Aggiorniamo i mock_input con i valori dello scenario corrente
                for field, value in input_values.items():
                    self.mock_inputs[field].text.return_value = value

                # Resettiamo i mock per ogni subTest
                self.mock_controller.reset_mock()
                self.mock_contract_view.reset_mock()

                self.dialog.addi_contract(
                    self.mock_inputs["user"],
                    self.mock_inputs["auto"],
                    self.mock_inputs["start_date"],
                    self.mock_inputs["end_date"],
                    self.mock_inputs["cauzione"],
                    self.mock_inputs["prezzo"],
                    self.mock_inputs["durataGaranzia"],
                    self.mock_inputs["tipoGaranzia"],
                    self.mock_inputs["kmMax"]
                )

                if should_call:
                    self.mock_controller.addo_noleggio_contratto.assert_called_once()
                    self.mock_contract_view.refresh_contracts.assert_called_once()
                else:
                    self.mock_controller.addo_noleggio_contratto.assert_not_called()
                    self.mock_contract_view.refresh_contracts.assert_not_called()


if __name__ == "__main__":
    unittest.main()
