from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:  # 开启事务
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)
