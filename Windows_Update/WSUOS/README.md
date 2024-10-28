# Windows Security Update Offline Service (WSUOS)

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

