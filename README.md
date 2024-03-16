# Anchor

🔥 Spreadsheet management tool server in python 🔥

<img width="1586" alt="image" src="https://github.com/Baluf/anchor/assets/162377261/7bc10cf9-8b5a-4614-92a2-94bc742cb3ab">


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Installation](#installation)

## Introduction

Anchor spreadsheet management server provides multiple capabilitis.<br>With this tool you can optimise your work with sheets, create, edit and save.<br> 
Below you can get more details of the usage :relaxed: <br>The server is written in python 3.9 and use Flask infrastructure. 

## Features

There are 3 main http handlers to the server detailed below:

- API :one: that receives aschema for the new sheet to be created. example for schema to be sent:
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

  
- API :two: that set a specific cell’s value in a specific sheet.
- API :three: that return a sheet by id. example for respone:
  
  ```json
  {
    "data": [
        [
            "A",
            "B",
            "C",
            "D"
        ],
        [
            "TRUE",
            null,
            null,
            null
        ],
        [
            "TRUE",
            "3",
            null,
            null
        ]
    ]
}  
    ```
  

## Endpoints

:one: GET http://localhost:5000/sheet/{sheetId} <br>
:two: POST http://localhost:5000/sheet <br>
:three: PUT http://localhost:5000/sheet/{sheetId}/cell <br>

## Installation :open_file_folder:

```bash
pip install -r requirements.txt
/usr/bin/python3.9 <your-project-path>/anchor/app.py
