from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import bindparam
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from backend.log import log
from backend.db.session import session

class ModelAdmin:

    def as_dict(self):
        detail = {}
        for col in self.__table__.columns:
            if str(col.type).lower().startswith('date'):
                detail[col.name] = str(getattr(self, col.name))
            else:
                detail[col.name] = getattr(self, col.name)

        return detail

    @classmethod
    async def insert(cls, extra={}, **kwargs):
        query = insert(cls).values(**kwargs)
        try:
            log.info(f'''Insert query with attrs={ str(kwargs) } extra={str(extra)}''')
            session.execute(query)
            session.commit()
        except Exception as e:
            session.rollback()
            log.error(f'Failed insert query due to error={str(e)} in {cls.__class__.__name__} with attrs={ str(kwargs) } extra={str(extra)}')
            raise Exception(str(e))
        return session

    @classmethod
    async def update(cls, extra={}, conditions={}, **kwargs):
        filters = []
        if len(conditions):
            for column in conditions:
                filters.append((getattr(cls, column) == f'''{conditions[column]}'''))

        query = update(cls).where(and_(*filters)).values(**kwargs)
        try:
            log.info(f'''Update query with attrs={ str(kwargs) } extra={str(extra)}''')
            session.execute(query)
            session.commit()
        except NoResultFound:
            session.rollback()
            raise NoResultFound('No result found')
        except Exception as e:
            log.error(f'Failed update query due to error={str(e)} in {cls.__class__.__name__} with attrs={ str(kwargs) } extra={str(extra)}')
            session.rollback()
            raise e
        return session

    @classmethod
    async def get(cls, extra={}, columns=None, **conditions):
        filters = []

        if len(conditions):
            for column in conditions:
                filters.append((getattr(cls, column) == f'''{conditions[column]}'''))

        try:
            log.info(f'''Select query with attrs={ str(conditions) } extra={str(extra)}''')
            if columns is None:
                query = select(cls).where(and_(*filters))
            else:
                query = select(cls).with_only_columns(*columns).where(and_(*filters))
            data = session.execute(query)
            result = [ entry for entry in data ]
            if not result:
                raise NoResultFound('No result found')
            return result
        except Exception as e:
            log.error(f'Failed select query due to error={str(e)} extra={str(extra)}')
            session.rollback()
            raise e  

    @classmethod
    async def delete(cls, extra={}, conditions={}):
        filters = []
        
        if len(conditions):
            for column in conditions:
                filters.append((getattr(cls, column) == f'''{conditions[column]}'''))

        query = delete(cls).where(and_(*filters))
        try:
            log.info(f'''Delete query extra={str(extra)}''')
            session.execute(query)
            session.commit()
        except NoResultFound:
            session.rollback()
            raise NoResultFound
        except Exception as e:
            log.error(f'Failed to delete  due to error={str(e)} extra={str(extra)}')
            session.rollback()
            raise Exception(str(e))
        return session