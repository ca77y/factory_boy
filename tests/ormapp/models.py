# Copyright: See the LICENSE file.
import tempfile

"""Helpers for testing ORM apps."""

import databases
import orm
import sqlalchemy

tmp_dir = tempfile.gettempdir()
database = databases.Database(f"sqlite:////{tmp_dir}/orm_test.db", force_rollback=True)
metadata = sqlalchemy.MetaData()


class Note(orm.Model):
    __tablename__ = "notes"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    text = orm.String(max_length=100)
    completed = orm.Boolean(default=False)


# Create the database
engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)
