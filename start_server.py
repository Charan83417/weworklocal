#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weworklocal.settings')
    
    print("Starting Django server...")
    print("Django version:", django.get_version())
    
    try:
        # Run migrations first
        print("Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Start the server
        print("Starting server on http://127.0.0.1:8000")
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
        
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to continue...")
