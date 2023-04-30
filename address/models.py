import datetime

from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from geoalchemy2 import functions as func
from sqlalchemy.future import select

from backend.db.base import ModelAdmin
from backend.db.session import Base
from backend.db.session import session
from sqlalchemy.orm.exc import NoResultFound
from backend.log import log

class Address(Base, ModelAdmin):
    __tablename__ = "address"

    id = Column(Integer, unique=True, primary_key=True, index=True, nullable=False)
    house_no = Column(String(250), nullable=False)
    street = Column(String(250), nullable=False)
    locality = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    postal_code = Column(String(250), nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    country = Column(String(250), nullable=False)
    email = Column(String(250), ForeignKey("users.email"), index=True)
    modified_date = Column(DateTime(timezone=True), default=datetime.datetime.now().utcnow, onupdate=datetime.datetime.now().utcnow)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now().utcnow, nullable=False)

    def __repr__(self):
        return (f"<{self.__class__.__name__}:{self.email}>")
    
    @classmethod
    async def get_nearby_loc(cls, extra={}, columns=None, **conditions):
        filters = []

        print(conditions)

        lat = conditions.pop('lat')
        lng = conditions.pop('lng')
        distance = conditions.pop('distance')

        filters.append((func.ST_Distance( func.ST_Point(cls.lng, cls.lat), func.ST_Point(lng, lat) ) <= distance))

        if len(conditions):
            for column in conditions:
                filters.append((getattr(cls, column) == f'''{conditions[column]}'''))

        try:
            log.info(f'''Select query with attrs={ str(conditions) } extra={str(extra)}''')
            query = select(cls).where(and_(*filters))
            # query = select(func.ST_Distance( func.ST_Point(cls.lng, cls.lat), func.ST_Point(lng, lat) ), distance)
            print(query)
            data = session.execute(query)
            result = [ entry for entry in data ]
            if not result:
                raise NoResultFound('No result found')
            return result
        except Exception as e:
            log.error(f'Failed select query due to error={str(e)} extra={str(extra)}')
            session.rollback()
            raise e  