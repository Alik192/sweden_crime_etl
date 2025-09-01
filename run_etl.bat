@echo off
cd /d "C:\Users\alikh\Desktop\sweden_crime_etl"
call .venv\Scripts\activate.bat
python main.py
deactivate
