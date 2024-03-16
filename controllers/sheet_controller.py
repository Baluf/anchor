import http
from flask import request, jsonify

from services import management_service


class SheetController:
    def __init__(self):
        self.management = management_service.ManagementService()

    def get_sheet(self, sheet_id):
        exit_code, msg = self.management.evaluate_sheet_content(sheet_id)
        if exit_code == -1:
            return jsonify(msg), http.HTTPStatus.BAD_REQUEST
        else:
            return jsonify({"data": msg}), http.HTTPStatus.OK

    def create_sheet(self):
        schema = request.json
        if 'columns' not in schema:
            return jsonify({"error": "Invalid schema, check again"}), http.HTTPStatus.BAD_REQUEST

        sheet_id, msg = self.management.create_new_sheet(columns=[row.get('name') for row in schema.get('columns')],
                                                         schema=schema)
        if sheet_id:
            return jsonify({"sheet_id": sheet_id}), http.HTTPStatus.CREATED
        else:
            return jsonify({"error": msg}), http.HTTPStatus.BAD_REQUEST

    def set_cell_endpoint(self, sheet_id):
        data = request.json

        if any(map(lambda key: key not in data, ['column', 'row_index', 'value'])) or data is None:
            return jsonify({"error": "Invalid request data"}), http.HTTPStatus.BAD_REQUEST

        try:
            row_index = int(data['row_index'])
        except Exception:
            return jsonify({"error": "Invalid row_index type should be int"}), http.HTTPStatus.BAD_REQUEST

        value = data['value']
        column_name = data['column']

        exit_code, msg = self.management.update_sheet_cell(sheet_id, column_name, row_index, value)

        if exit_code == -1:
            return jsonify(msg), http.HTTPStatus.BAD_REQUEST
        else:
            return jsonify(msg), http.HTTPStatus.OK
