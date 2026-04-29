import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR  = os.path.join(BASE_DIR, "app")
sys.path.insert(0, APP_DIR)

from main import main

if __name__ == "__main__":
    main()

