# anchor
spreadsheet management server in python.

# anchor - spreadsheet management

<img width="1575" alt="image" src="https://github.com/Baluf/anchor/assets/162377261/2e56c3df-45d9-4754-bb72-24dd4c8dc52a">


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)

## Introduction

Flask server in python which provides spreadsheet management login. <br> With the server you can create, edit, get the sheets.

## Features

There are 3 main http handlers to the project detailed below:

- API that receives aschema for the new sheet to be created.
```json
{
"columns":[
{
"name":"A",
"type":"boolean"
},
{
"name":"B",
"type":"int"
},
{
"name":"C",
"type":"double"
},
{
"name":"D",
"type":"string"
}
]
}
```

  
- API that set a specific cell’s value in a specific sheet.
- API that return a sheet by id.

## Endpoints

1. @sheet_blueprint.route('/sheet/<sheet_id>', methods=['GET'])
2. @sheet_blueprint.route('/sheet', methods=['POST'])
4. @sheet_blueprint.route('/sheet/<sheet_id>/cell', methods=['PUT'])

## Installation

```bash
pip install -r requirements.txt
/usr/bin/python3 <your-project-path>/anchor/app.py
