import sqlalchemy

import sqlalchemy.orm as _orm
from decouple import config

DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}" \
               f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"

engine = sqlalchemy.create_engine(DATABASE_URL)

LocalSession = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
