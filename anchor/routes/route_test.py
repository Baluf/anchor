import http
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from routes.route import sheet_blueprint


class TestSheetRoutes(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(sheet_blueprint)

        self.mock_sheet_controller = MagicMock()

    def test_get_sheet_route(self):
        self.mock_sheet_controller.get_sheet.return_value = {'msg': 'Success'}
        with patch('routes.route.sc', new=self.mock_sheet_controller):
            with self.app.test_client() as client:
                response = client.get('/sheet/50a44046-ed9a-408e-b6d1-165cae9a1ca0')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['msg'], 'Success')
                self.mock_sheet_controller.get_sheet.assert_called_once_with('50a44046-ed9a-408e-b6d1-165cae9a1ca0')

    def test_create_sheet_route(self):
        self.mock_sheet_controller.create_sheet.return_value = {"sheet_id": '50a44046-ed9a-408e-b6d1-165cae9a1ca0'}

        with patch('routes.route.sc', new=self.mock_sheet_controller):
            with self.app.test_client() as client:
                response = client.post('/sheet', json={"columns": [{
                    "name": "A",
                    "type": "boolean"},
                    {
                        "name": "B",
                        "type": "int"
                    },
                    {
                        "name": "C",
                        "type": "double"
                    },
                    {
                        "name": "D",
                        "type": "string"
                    }
                ]})
                self.assertEqual(response.status_code, 200)
                self.mock_sheet_controller.create_sheet.assert_called_once()

    def test_set_cell_endpoint_route(self):
        self.mock_sheet_controller.set_cell_endpoint.return_value = {"Result": "Success"}

        with patch('routes.route.sc', new=self.mock_sheet_controller):
            with self.app.test_client() as client:
                response = client.put('/sheet/50a44046-ed9a-408e-b6d1-165cae9a1ca0/cell')
                self.assertEqual(response.status_code, 200)
                self.mock_sheet_controller.set_cell_endpoint.assert_called_once()


if __name__ == '__main__':
    unittest.main()
