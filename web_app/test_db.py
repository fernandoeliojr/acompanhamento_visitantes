import sys
import os

# Add the directory to the path so we can import from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from flask import Flask
from database import init_db, verify_db_creation

app = Flask(__name__, instance_relative_config=True)
app.instance_path = os.path.join(os.getcwd(), 'instance')

init_db(app)

if verify_db_creation(app):
    print("SUCCESS: Database created.")
    sys.exit(0)
else:
    print("FAILURE: Database not created.")
    sys.exit(1)
