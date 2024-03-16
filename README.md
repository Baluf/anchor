# anchor
spreadsheet management server in python.

# anchor - spreadsheet management

![Uploading image.png…]()


## Table of Contents

- [Installation](#installation)
- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Endpoints](#endpoints)

## Introduction

Flask server in python which provides spreadsheet management login. <br> With the server you can create, edit, get the sheets.

## Features

There are 3 main http handlers to the project detailed below:

- API 1 that receives aschema for the new sheet to be created.
```json
{
    "columns": [
        {
            "name": "A",
            "type": "boolean"
        },
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
}
```

  
- API 2 that set a specific cell’s value in a specific sheet.
- API 3 that return a sheet by id.

## Endpoints

1. GET http://localhost:5000/sheet/{sheetId}
2. POST http://localhost:5000/sheet
4. PUT http://localhost:5000/sheet/<sheet_id>/cell

## Installation

```bash
pip install -r requirements.txt
/usr/bin/python3 <your-project-path>/anchor/app.py
