@echo off

cmd /k "cd venv\Scripts & activate & cd /d  ../.. & set FLASK_APP=app & flask run"
