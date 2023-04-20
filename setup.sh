#!/bin/bash

# Erstellen der virtuellen Umgebung
python3 -m venv venv

# Aktivieren der virtuellen Umgebung
source venv/bin/activate

# Installieren der benötigten Pakete
pip install -r requirements.txt

# Ausführen des Python-Skripts
python3 app.py
