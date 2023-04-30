from backend.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

settings = get_settings()
Base = declarative_base()

def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension(get_settings().SPATIALITE_PATH)

class DatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)
    
    def init(self):
        self._engine = create_engine(settings.DATABASE_URL)
        listen(self._engine, 'connect', load_spatialite)

        Session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        self._session = Session()

    def create_all(self):
            Base.metadata.create_all(self._engine)

    def get_session(self):
        return self._session
    

session = DatabaseSession()