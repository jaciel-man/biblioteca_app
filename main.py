import os
import sys
import flet as ft

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from biblioblog.model.database import Database
from biblioblog.view.app import main

if __name__ == '__main__':
    try:
        Database.initialize()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    
    ft.run(main)
