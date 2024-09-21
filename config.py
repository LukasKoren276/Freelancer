import os
from sqlalchemy import create_engine

app_folder = os.getcwd()
db_folder = os.path.join(app_folder, 'database')
db_file = os.path.join(db_folder, 'freelancer_db.sqlite')
engine = create_engine(f'sqlite:///{db_file}')
