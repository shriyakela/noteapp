# reset_db.py

from website import create_app, db
from website.models import User, Note  # Import your models here

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Create all tables
    print("All tables dropped and recreated.")
