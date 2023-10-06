from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)
import os
import logging

logger = logging.getLogger("uvicorn.run")

Base = declarative_base()
engine_params = {}

def _build_local():
    logger.info(f"Database: Using local SQLite for Unittests")
    if os.environ.get('PWD').endswith("tests"):
        SQLALCHEMY_DATABASE_URL = "sqlite:///./unittest.db"
    else:
        SQLALCHEMY_DATABASE_URL = "sqlite:///tspycher.db"
        
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
    )

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                           bind=engine))
    from tspycher.api.models.track import TeltonikaTrack
    meta = MetaData(bind=engine)
    meta.create_all(tables=[TeltonikaTrack.__table__])
    return db_session

def _build_bigquery():
    bigquery_project = "tspycher"
    bigquery_dataset = os.environ.get('BIGQUERY_DATASET', 'teltonika_development')
    bigquery_engine_url = f'bigquery://{bigquery_project}/{bigquery_dataset}'

    logger.info(f"Database: Using bigquery Engine url: {bigquery_engine_url}")
    engine = create_engine(bigquery_engine_url, **engine_params)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=engine))
    return db_session


def get_db():
    try:
        if os.environ.get('PWD').endswith("tests"):
            db = _build_local()
        else:
            if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or os.environ.get('BIGQUERY_DATASET'):
                db = _build_bigquery()
            else:
                db = _build_local()
        yield db
    finally:
        db.close()