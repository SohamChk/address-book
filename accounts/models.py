import datetime

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime

from backend.db.base import ModelAdmin
from backend.db.session import Base

class Users(Base, ModelAdmin):
    __tablename__ = "users"

    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, primary_key=True, index=True, nullable=False)
    password = Column(String(250), nullable= False)
    modified_date = Column(DateTime(timezone=True), default=datetime.datetime.now().utcnow, onupdate=datetime.datetime.now().utcnow)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now().utcnow, nullable=False)

    def __repr__(self):
        return (f"<{self.__class__.__name__}:{self.email}>")