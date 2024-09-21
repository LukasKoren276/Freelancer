import os
from config import db_file, db_folder, engine
from models import Base


def initialize_db():
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    if not os.path.exists(db_file):
        print(f"Database file not found. Creating new database... ", end='')
        Base.metadata.create_all(engine)
        print(f"Database initialized and tables created at: {db_file}")
