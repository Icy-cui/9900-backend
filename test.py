import sqlalchemy
from sqlalchemy.sql import text

engine = sqlalchemy.create_engine('sqlite:///instance/test.db', echo=True)

conn = engine.connect()
conn.execute(text('DROP TABLE test;'))
conn.close()
