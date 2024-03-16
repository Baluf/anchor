import os
from typing import Union

import jsonschema
from loaders import sheet_loader as shl
from loaders import schema_loader as scl

from constants import SHEETS_FILES_LOCATION, SCHEMA_FILES_LOCATION
from loaders.Exceptions import *

columns_structure = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "type": {"type": "string"},
    },
    "required": ["name", "type"],
}


class ManagementService:
    def __init__(self, sheets_directory=SHEETS_FILES_LOCATION, schema_directory=SCHEMA_FILES_LOCATION):

        if not os.path.exists(sheets_directory):
            os.makedirs(sheets_directory)

        if not os.path.exists(schema_directory):
            os.makedirs(schema_directory)

        self.sheet_loader = shl.SheetLoader(sheets_directory)
        self.schema_loader = scl.SchemaLoader(schema_directory)

    def update_sheet_cell(self, sheet_id: str, column_name: str, row_index: int, value: str):
        if row_index < 1:
            return -1, {"error": "invalid row_index"}

        sheet_path = self.sheet_loader.get_sheet_path_by_id(sheet_id)
        schema = self.schema_loader.get_schema_by_id(sheet_id)

        if schema is None:
            return -1, {"error": "Schema not found"}

        if sheet_path is None:
            return -1, {"error": "Sheet not found"}

        try:
            column_index = [c.get('name') for c in schema.get('columns')].index(column_name)
        except ValueError:
            return -1, {"error": "Column not found"}

        if self.validate_value_type(sheet_id, value, schema.get('columns')[column_index].get('type')) is True:
            try:
                self.sheet_loader.update_sheet_cell(sheet_id, row_index, column_index, value)
                return 1, {"Result": "Success"}
            except UpdateSheetCellException:
                pass
        return -1, {"error": "Value is not standing with schema requirements"}

    def validate_value_type(self, sheet_id: str, value: str, column_type: str) -> bool:
        if value.startswith('lookup'):
            if self.get_lookup_cell_type(sheet_id, value) == column_type:
                return True
        if column_type == "boolean":
            return value.lower() == "true" or value.lower() == "false"
        elif column_type == "int":
            return str.isdigit(value)
        elif column_type == "double":
            try:
                float(value)
                return True
            except ValueError:
                return False
        elif column_type == "string":
            return isinstance(value, str)
        else:
            return False

    def get_lookup_cell_type(self, sheet_id: str, lookup_function: str) -> Union[None, str]:
        lookup_args = lookup_function.strip().split("(")[1][:-1].split(",")
        if len(lookup_args) != 2:
            return None
        column_name = lookup_args[0].strip('"“”')
        schema = self.schema_loader.get_schema_by_id(sheet_id)
        for col in schema.get('columns'):
            if col.get('name') == column_name:
                return col.get('type')

        return None

    def evaluate_sheet_content(self, sheet_id: str) -> (int, Union[dict, list]):
        sheet_path = self.sheet_loader.get_sheet_path_by_id(sheet_id)
        schema = self.schema_loader.get_schema_by_id(sheet_id)

        if sheet_path is None or schema is None:
            return -1, {"error": "Sheet or Schema not found"}

        evaluated_data = []
        visited = set()
        evaluated_values = {}

        for row_index, row in enumerate(self.sheet_loader.get_sheet_generator(sheet_id), start=1):
            evaluated_row = []
            for col_index, value in enumerate(row, start=1):
                if isinstance(value, str) and value.startswith('lookup'):
                    if self.is_circular_reference(sheet_id, value, visited):
                        evaluated_row.append(f"Error: Circular reference detected for {value}")
                        continue

                    result = self.evaluate_lookup_recursive(sheet_id, value, evaluated_values)
                    if result is not None:
                        evaluated_row.append(result)
                    else:
                        evaluated_row.append(f"Error: Lookup failed for {value}")
                else:
                    evaluated_row.append(value)
            evaluated_data.append(evaluated_row)

        return 1, evaluated_data

    def is_circular_reference(self, sheet_id: str, lookup_function: str, visited: set) -> bool:
        if lookup_function in visited:
            return True

        visited.add(lookup_function)
        result = self.evaluate_lookup(sheet_id, lookup_function)

        if isinstance(result, str) and result.startswith('lookup'):
            if self.is_circular_reference(sheet_id, result, visited):
                return True

        visited.remove(lookup_function)
        return False

    def evaluate_lookup_recursive(self, sheet_id: str, lookup_function: str, evaluated_values: dict):
        if lookup_function in evaluated_values:
            return evaluated_values[lookup_function]
        result = self.evaluate_lookup(sheet_id, lookup_function)
        if isinstance(result, str) and result.startswith('lookup'):
            result = self.evaluate_lookup_recursive(sheet_id, result, evaluated_values)
        evaluated_values[lookup_function] = result
        return result

    def evaluate_lookup(self, sheet_id: str, lookup_function: str):
        lookup_args = lookup_function.strip().split("(")[1][:-1].split(",")
        if len(lookup_args) != 2:
            return None

        column_name = lookup_args[0].strip('"“”')
        row_index = int(lookup_args[1])

        try:
            value = self.sheet_loader.get_cell_value(sheet_id, column_name, row_index)
            return value
        except SheetGetValueException:
            return None

    def create_new_sheet(self, columns: list, schema: dict) -> (Union[str, None], str):
        try:
            for column in schema['columns']:
                jsonschema.validate(instance=column, schema=columns_structure)
        except jsonschema.exceptions.ValidationError:
            return None, "sheet is invalid with its schema"

        try:
            sheet_id = self.sheet_loader.create(columns)
        except SheetCreationException:
            return None, "problem while creation new sheet"

        self.schema_loader.create(sheet_id, schema)

        try:
            self.schema_loader.save(sheet_id, schema)
        except SchemaSaveException:
            return None, "problem while saving sheet file"

        return sheet_id, None
