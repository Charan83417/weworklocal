@echo off
cd /d C:\weworkweb
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
pause
