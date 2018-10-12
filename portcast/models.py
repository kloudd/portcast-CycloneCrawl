"""
    This is the Model file. ORM base for the postgres database.
    crawled data goes into Scrapy object and then send in the pipeline to a model object.
    - Sumit Singh Kanwal
"""

from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, DateTime, Text)

from scrapy.utils.project import get_project_settings

DECLARATIVEBASE = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    """
    Creates the table if not present.
    """

    DECLARATIVEBASE.metadata.create_all(engine)


class CycloneDB(DECLARATIVEBASE):
    """
    Model class for Cyclone - db_table_name: cyclone
    """
    __tablename__ = "cyclone"

    id = Column(Integer, primary_key=True)
    name = Column('name', Text())


class CycloneForecastDB(DECLARATIVEBASE):
    """
    Model class for CycloneForecast - db_table_name: cyclone_forecast
    """
    __tablename__ = "cyclone_forecast"

    id = Column(Integer, primary_key=True)
    cyclone_id = Column(Integer, ForeignKey(CycloneDB.id))
    time_of_forecast = Column('time_of_forecast', Text())


class CycloneTrackHistoryDB(DECLARATIVEBASE):
    """
    Model class for CycloneTrackHistory - db_table_name: cyclone_track_history
    """
    __tablename__ = "cyclone_track_history"

    id = Column(Integer, primary_key=True)
    cyclone_id = Column(Integer, ForeignKey(CycloneDB.id))
    synoptic_time = Column('synoptic_time', DateTime())
    latitude = Column('latitude', Integer())
    longitude = Column('longitude', Integer())
    intensity = Column('intensity', Integer())


class ForecastTrackDB(DECLARATIVEBASE):
    """
    Model class for ForecastTrack - db_table_name: forecast_track
    """
    __tablename__ = "forecast_track"

    id = Column(Integer, primary_key=True)
    cyclone_forecast_id = Column(Integer, ForeignKey(CycloneForecastDB.id))
    forecast_hour = Column('forecast_hour', Text())
    latitude = Column('latitude', Integer())
    longitude = Column('longitude', Integer())
    intensity = Column('intensity', Integer())
