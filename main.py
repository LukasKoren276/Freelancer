import os
from sqlalchemy.orm import sessionmaker
from models import Base

from config import db_file, engine
from controllers.guiController import GuiController
from controllers.databaseManager import DatabaseManager


def initialize_db():
    if not os.path.exists(db_file):
        print(f"Database file not found. Creating new database... ", end='')
        Base.metadata.create_all(engine)
        print(f"Database initialized and tables created at: {db_file}")


def start_application():
    try:
        initialize_db()
    except Exception as err:
        print(f'An exception of the type {type(err)} happened.\n Message: {err} \n Cause: {err.__cause__}')

    Session = sessionmaker(bind=engine)
    session = Session()
    database_manager = DatabaseManager(session)
    controller = GuiController(database_manager)
    controller.open_main_window()


if __name__ == "__main__":
    start_application()
