@echo off

REM Erstellen der virtuellen Umgebung
python -m venv venv

REM Aktivieren der virtuellen Umgebung
call venv\Scripts\activate.bat

REM Installieren der benötigten Pakete
pip install -r requirements.txt

REM Ausführen des Python-Skripts
python app.py
