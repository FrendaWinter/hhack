# Windows Security Update Offline Service (WSUOS)

## Table of Contents

- [Windows Security Update Offline Service (WSUOS)](#windows-security-update-offline-service-wsuos)
  - [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Structure of wsusscn2.cab file](#structure-of-wsusscn2cab-file)
  - [Structure format](#structure-format)
  - [Details Content](#details-content)
    - [`Index.xml` file](#indexxml-file)
    - [`Package.cab` file](#packagecab-file)
      - [The `package.xml` file](#the-packagexml-file)


# Introduction

Script convert wsusscn2.cab file to easy to use database.

- SQL lite
- [7 Zip](https://www.7-zip.org/download.html)
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [Python](https://www.python.org/)


1. Create new python virtual environment `python -m venv wsuos`
2. Active virtual environment `.\wsuos\Scripts\Activate.ps1` (Windows PowerShell) or `source wsuos/bin/activate` (bash)
3. Run `python main.py`
4. Wait for script to finish
5. Open `updates.db` in DB Browser for SQLite

# Structure of wsusscn2.cab file

## Structure format

The `wsusscn2.cab` file contains the following files and folders:

- An `Index.xml` file
- A `Package.cab` file
  - The `package.xml` file
- Other `*.cab` files with numbered names
  - The `C` folder
  - The `E` folder
  - The `Files` folder
  - The `I` folder
  - The `X` folder

## Details Content 

### `Index.xml` file

The file contains information about the index of all updates in the `wsusscn2.cab` file.

Take a look at the `CABLIST` tag in the `Index.xml` file.

```
<CAB NAME="package2.cab" RANGESTART="0" FILESDIR="1"/>
<CAB NAME="package3.cab" RANGESTART="170753"/>
<CAB NAME="package4.cab" RANGESTART="258633"/>
<CAB NAME="package5.cab" RANGESTART="334658"/>
```

This mean that there are 4 `CAB` files in the `wsusscn2.cab` file. 
- The first one starts at index `0`, that mean it contains data of update id that have revision id `0` to `170752`, one number behind of the range start of the next package. 
- The second one starts at index `170753`, that mean it contains data of update id that have revision id from `170753` to `258632`, one number behind of the range start of the next package. And so on.

### `Package.cab` file

The `Package.cab` file contains `package.xml` file. This file contains metadata of all updates in the `wsusscn2.cab` file.

#### The `package.xml` file

The `package.xml` file contains metadata of all updates.

`<?xml version="1.0" encoding="utf-8"?>`
- xml version `1.0`
- encoding `utf-8`

Python code to parse the `package.xml` file:
```python
import xml.etree.ElementTree as ET

root = ET.parse(current_file, parser = ET.XMLParser(encoding = 'utf-8'))
```

Take a look at the `Updates` tag in the `package.xml` file.

```xml
<?xml version="1.0" encoding="utf-8"?>
<OfflineSyncPackage ...> 
	<Updates> ## Contains all updates metadata
		<Update ...> ## Contains metadata of one update
            ...
        </Update>
    </Updates>
    <FileLocations> ## Contains all file locations of updates
        <FileLocation ... /> ## ID and Url
    </FileLocations>
</OfflineSyncPackage>
```

Some important properties of the `Update` tag:
- `RevisionId`: The revision id of the update. It is unique for each update. Refers to the number in `index.xml` file.
- `DeploymentAction`: The deployment action of the update. If it is `Bundle` it means that the update is a bundle.

