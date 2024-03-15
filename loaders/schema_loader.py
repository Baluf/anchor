import json
import os
from constants import SCHEMA_FILES_LOCATION
from .Exceptions import *


class SchemaLoader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, directory=SCHEMA_FILES_LOCATION):
        if not hasattr(self, 'schemas'):
            self.schemas = {}
        if not hasattr(self, 'locks'):
            self.locks = {}
        if not hasattr(self, 'directory'):
            self.directory = directory

    def create(self, sheet_id: str, schema: dict):
        self.schemas[sheet_id] = schema

    def get_schema_by_id(self, schema_id):
        if not self.schemas:
            self.load_schemas()
        return self.schemas.get(schema_id)

    def load_schemas(self):
        try:
            files = os.listdir(self.directory)
            for file in files:
                with open(os.path.join(self.directory, file), 'r') as json_file:
                    data = json.load(json_file)
                    self.schemas[file.split('.')[0]] = data
        except Exception:
            raise SchemaLoadException()

    def save(self, sheet_id: str, schema: dict):
        try:
            with open(os.path.join(self.directory, f"{sheet_id}.json"), 'w') as json_file:
                json_file.write(json.dumps(schema))
            self.schemas[sheet_id] = schema
        except Exception:
            raise SchemaSaveException()
