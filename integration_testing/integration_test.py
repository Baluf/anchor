from integration_testing.test_base import BaseTestCase
import uuid


class IntegrationTest(BaseTestCase):
    shared_data = {}

    def test_create_simple_sheet(self):
        response = self.client.post('http://127.0.0.1:5000/sheet', json={
            "data": {
                "A": "true",
                "B": 5,
                "C": 23.4,
                "D": "Bar Al"
            }, "columns": [{
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
            ]
        })
        self.assertTrue(response.status_code == 201)
        self.assertTrue(is_valid_uuid(response.json.get("sheet_id")))
        self.shared_data["sheet_id"] = response.json.get("sheet_id")

    def test_get_sheet_content(self):
        if self.shared_data.get("sheet_id") is None:
            raise Exception("No sheet_id found")  # The test_create_simple_sheet is prerequisite

        response = self.client.get(f'http://127.0.0.1:5000/sheet/{self.shared_data["sheet_id"]}')
        self.assertTrue(response.status_code == 200)

    def test_edit_sheet_content(self):
        if self.shared_data.get("sheet_id") is None:
            raise Exception("No sheet_id found")  # The test_create_simple_sheet is prerequisite

        response = self.client.put(f'http://127.0.0.1:5000/sheet/{self.shared_data["sheet_id"]}/cell', json={
            "column": "A",
            "row_index": "1",
            "value": "true"
        })
        self.assertTrue(response.status_code == 200)


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
