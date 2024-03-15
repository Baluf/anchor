import os
import unittest

from services.management_service import ManagementService


class ManagementServiceTest(unittest.TestCase):
    SHEETS_LOCATION = "../testing/excel_files"
    SCHEMA_LOCATION = "../testing/schema_files"

    def setUp(self):
        if not os.path.exists(ManagementServiceTest.SHEETS_LOCATION):
            os.makedirs(ManagementServiceTest.SHEETS_LOCATION)

        if not os.path.exists(ManagementServiceTest.SCHEMA_LOCATION):
            os.makedirs(ManagementServiceTest.SCHEMA_LOCATION)

        self.service = ManagementService(ManagementServiceTest.SHEETS_LOCATION, ManagementServiceTest.SCHEMA_LOCATION)
        self.columns = ['A', 'B', 'C', 'D']
        self.schema = {
            'columns': [{'name': 'A', 'type': 'boolean'}, {'name': 'B', 'type': 'int'}, {'name': 'C', 'type': 'double'},
                        {'name': 'D', 'type': 'string'}]}

    def test_create_sheet(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        self.assertIsNotNone(sheet_id)

    def test_create_sheet_validate_schema(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        schema = self.service.schema_loader.get_schema_by_id(sheet_id)
        self.assertEqual(self.schema, schema)

    def test_update_cell(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        res = self.service.update_sheet_cell(sheet_id, 'A', 2, 'true')
        self.assertTrue(res[0] == 1)

    def test_update_cell_with_wrong_value_type(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        res = self.service.update_sheet_cell(sheet_id, 'A', 2, 'wrong_value')
        self.assertTrue(res[0] == -1)

    def test_update_cell_with_not_exist_column(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        res = self.service.update_sheet_cell(sheet_id, 'M', 2, 'wrong_value')
        self.assertTrue(res[0] == -1)

    def test_update_cell_with_lookup_func_and_evaluate_content(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        self.service.update_sheet_cell(sheet_id, 'A', 2, 'true')
        self.service.update_sheet_cell(sheet_id, 'A', 3, "lookup(“A”,2)")
        _, data = self.service.evaluate_sheet_content(sheet_id)
        self.assertTrue(data[1][0] == 'true')
        self.assertTrue(data[2][0] == 'true')

    def test_update_cell_with_lookup_func_with_cycle_size_1(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        self.service.update_sheet_cell(sheet_id, 'A', 2, 'lookup(“A”,3)')
        self.service.update_sheet_cell(sheet_id, 'A', 3, "lookup(“A”,2)")
        _, data = self.service.evaluate_sheet_content(sheet_id)
        self.assertTrue(data[1][0] == 'Error: Circular reference detected for lookup(“A”,3)')
        self.assertTrue(data[2][0] == 'Error: Circular reference detected for lookup(“A”,2)')

    def test_update_cell_with_lookup_func_with_cycle_size_3(self):
        sheet_id, _ = self.service.create_new_sheet(self.columns, self.schema)
        self.service.update_sheet_cell(sheet_id, 'A', 2, 'lookup(“A”,3)')
        self.service.update_sheet_cell(sheet_id, 'A', 3, "lookup(“A”,4)")
        self.service.update_sheet_cell(sheet_id, 'A', 4, "lookup(“A”,2)")

        _, data = self.service.evaluate_sheet_content(sheet_id)
        self.assertTrue(data[1][0] == 'Error: Circular reference detected for lookup(“A”,3)')
        self.assertTrue(data[2][0] == 'Error: Circular reference detected for lookup(“A”,4)')
        self.assertTrue(data[3][0] == 'Error: Circular reference detected for lookup(“A”,2)')

    def tearDown(self):
        # delete all files we created in tests.
        for filename in os.listdir(ManagementServiceTest.SHEETS_LOCATION):
            os.remove(os.path.join(ManagementServiceTest.SHEETS_LOCATION, filename))

        for filename in os.listdir(ManagementServiceTest.SCHEMA_LOCATION):
            os.remove(os.path.join(ManagementServiceTest.SCHEMA_LOCATION, filename))

