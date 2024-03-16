# Anchor

🔥 Spreadsheet management tool server in python 🔥

<img width="1586" alt="image" src="https://github.com/Baluf/anchor/assets/162377261/7bc10cf9-8b5a-4614-92a2-94bc742cb3ab">


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Endpoints](#endpoints)
- [Installation](#installation) :open_file_folder:

## Introduction

Anchor spreadsheet management server provides multiple capabilitis.<br>With this tool you can optimise your work with sheets. Create, edit and store them.<br> 
The server is written in python 3.9 and use Flask infrastructure.<br>Below you can get more details of the usage :relaxed: 

## Features

There are 3️⃣ main http handlers to the server detailed below:

- API 1️⃣ that receives a schema json (Content-Type: application/json) for the new sheet to be created.<br>Example for schema to be sent **(please add header of Content-Type: application/json)**:
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

  
- API 2️⃣ that set a specific cell’s value in a specific sheet.<br> Example for json to be sent **(please add header of Content-Type: application/json)**:
 ```json
{
    "column": "A",
    "row_index": "1",
    "value": "true"
}
```
- API 3️⃣ that returns a sheet by id. <br> Example for respone in json:
```json
{
"data": [["A","B","C","D"],
        ["TRUE",null,null,null],
        ["TRUE","3",null,null]]
}
```
  

## Endpoints

1️⃣ GET http://localhost:5000/sheet/{sheetId} <br>
2️⃣ POST http://localhost:5000/sheet <br>
3️⃣ PUT http://localhost:5000/sheet/{sheetId}/cell <br>

## Installation 

Make sure you have python 🐍 3.9 or higher installed on your machine 

Then install requirements using pip:
```bash
pip install -r requirements.txt
```

To run the server execute:

```bash
/usr/bin/python3.9 <your-project-path>/anchor/app.py
```
