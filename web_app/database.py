import sqlite3
import os
from models import db, Visitor

def init_db(app):
    """
    Initializes the SQLite database.
    """
    db_path = os.path.join(app.instance_path, 'visitors.db')

    # Ensure instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print(f"Database initialized at {db_path}")

def verify_db_creation(app):
    db_path = os.path.join(app.instance_path, 'visitors.db')
    return os.path.exists(db_path)
