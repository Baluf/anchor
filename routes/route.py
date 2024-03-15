from flask import Blueprint
from controllers.sheet_controller import SheetController

sheet_blueprint = Blueprint('sheet', __name__)

sc = SheetController()


@sheet_blueprint.route('/sheet/<sheet_id>', methods=['GET'])
def get_sheet_route(sheet_id):
    return sc.get_sheet(sheet_id)


@sheet_blueprint.route('/sheet', methods=['POST'])
def create_sheet_route():
    return sc.create_sheet()


@sheet_blueprint.route('/sheet/<sheet_id>/cell', methods=['PUT'])
def set_cell_endpoint_route(sheet_id):
    return sc.set_cell_endpoint(sheet_id)
