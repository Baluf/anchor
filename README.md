# Anchor

Spreadsheet management tool server in python.

<img width="1586" alt="image" src="https://github.com/Baluf/anchor/assets/162377261/7bc10cf9-8b5a-4614-92a2-94bc742cb3ab">


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Installation](#installation)

## Introduction

Anchor spreadsheet management server provides multiple capabilitis. <br> with this tool you can optimise your work with sheets, create, edit and save. 
Below you can get more details of the usage. <br>  The server is written in python 3.9 and use Flask infrastructure. 

## Features

There are 3 main http handlers to the project detailed below:

- API 1: that receives aschema for the new sheet to be created.
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

  
- API 2: that set a specific cell’s value in a specific sheet.
- API 3: that return a sheet by id.

## Endpoints

1. GET http://localhost:5000/sheet/{sheetId}
2. POST http://localhost:5000/sheet
4. PUT http://localhost:5000/sheet/{sheetId}/cell

## Installation

```bash
pip install -r requirements.txt
/usr/bin/python3.9 <your-project-path>/anchor/app.py
