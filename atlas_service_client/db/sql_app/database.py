import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
schema_name = 'test'
Base = declarative_base()
#if not engine.dialect.has_schema(engine, schema_name):
#    engine.execute(sqlalchemy.schema.CreateSchema(schema_name))

#try:
#    engine.execute(sqlalchemy.schema.CreateSchema(schema_name))
#    Base.metadata.schema = schema_name
#except sqlalchemy.exc.ProgrammingError:
#        pass



