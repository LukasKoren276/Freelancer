
from sqlalchemy.orm import sessionmaker
from config import engine
from db_initialize import initialize_db
from Gui import MainWindow


def start_application():
    try:
        initialize_db()
    except Exception as err:
        print(f'An exception of the type {type(err)} happened.\n Message: {err} \n Cause: {err.__cause__}')

    Session = sessionmaker(bind=engine)
    session = Session()
    app = MainWindow('INVOICER', session)
    app.mainloop()


if __name__ == "__main__":
    start_application()
