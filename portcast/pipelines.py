"""
    This is the pipeline file.
    All the scrapy items are passed on to pipeline to do operations after parsing.
    The scrapy items are parsed to the models.
    - Sumit Singh Kanwal
"""
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .models import db_connect, create_table, CycloneDB, CycloneForecastDB,\
    CycloneTrackHistoryDB, ForecastTrackDB
from .items import Cyclone, CycloneForecast, CycloneTrackHistory, ForecastTrack


class PortcastPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()
        quotedb = 0

        if isinstance(item, Cyclone):
            quotedb = self.handle_cyclone(item, spider, session)

        if isinstance(item, CycloneForecast):
            quotedb = self.handle_cyclone_forecast(item, spider, session)

        if isinstance(item, CycloneTrackHistory):
            quotedb = self.handle_cyclone_track_history(item, spider, session)

        if isinstance(item, ForecastTrack):
            quotedb = self.handle_forecast_track(item, spider, session)

        try:
            if quotedb != 0:
                session.add(quotedb)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

    def handle_cyclone(self, item, spider, session):
        """
        Process the cyclone item and is parsed/converted to the model object.
        Thereby saving in the database.
        """
        if session.query(CycloneDB.id).filter(CycloneDB.name == item["name"][0]).first():
            return 0

        cyclone_db_obj = CycloneDB()
        cyclone_db_obj.name = item["name"][0]

        return cyclone_db_obj

    def handle_cyclone_forecast(self, item, spider, session):
        """
        Process the CycloneForecast item and is parsed/converted to the model object.
        Thereby saving in the database.
        """
        cyclone_id = session.query(CycloneDB.id).filter(CycloneDB.name == item["name"][0]).first()

        if session.query(CycloneForecastDB.id)\
            .filter(CycloneForecastDB.time_of_forecast == item["time_of_forecast"][0])\
            .filter(CycloneForecastDB.cyclone_id == cyclone_id)\
            .first():
            return 0

        cyclone_db_obj = CycloneForecastDB()
        cyclone_db_obj.cyclone_id = cyclone_id
        cyclone_db_obj.time_of_forecast = item["time_of_forecast"][0]

        return cyclone_db_obj

    def handle_cyclone_track_history(self, item, spider, session):
        """
        Process the CycloneTrackHistory item and is parsed/converted to the model object.
        Thereby saving in the database.
        """
        cyclone_id = session.query(CycloneDB.id).filter(CycloneDB.name == item["name"][0]).first()

        if session.query(CycloneTrackHistoryDB.id)\
                .filter(CycloneTrackHistoryDB.cyclone_id == cyclone_id) \
                .filter(CycloneTrackHistoryDB.synoptic_time == item["synoptic_time"]) \
                .first():
            return 0

        cyclone_db_obj = CycloneTrackHistoryDB()
        cyclone_db_obj.cyclone_id = cyclone_id
        cyclone_db_obj.synoptic_time = datetime.strptime(item["synoptic_time"], '%Y%m%d%H%M')
        cyclone_db_obj.latitude = int(item["latitude"])
        cyclone_db_obj.longitude = int(item["longitude"])
        cyclone_db_obj.intensity = int(item["intensity"])

        return cyclone_db_obj

    def handle_forecast_track(self, item, spider, session):

        """
        Process the CycloneForecast item and is parsed/converted to the model object.
        Thereby saving in the database.
        """
        cyclone_id = session.query(CycloneDB.id).filter(CycloneDB.name == item["name"][0]).first()
        cyclone_forecast_id = session.query(CycloneForecastDB.id)\
                .filter(CycloneForecastDB.time_of_forecast == item["time_of_forecast"][0])\
                .filter(CycloneForecastDB.cyclone_id == cyclone_id)\
                .first()

        if session.query(ForecastTrackDB.id)\
                .filter(ForecastTrackDB.cyclone_forecast_id == cyclone_forecast_id)\
                .filter(ForecastTrackDB.forecast_hour == item["forecast_hour"])\
                .first():
            return 0

        cyclone_db_obj = ForecastTrackDB()
        cyclone_db_obj.cyclone_forecast_id = cyclone_forecast_id
        cyclone_db_obj.forecast_hour = item["forecast_hour"]
        cyclone_db_obj.latitude = int(item["latitude"])
        cyclone_db_obj.longitude = int(item["longitude"])
        cyclone_db_obj.intensity = int(item["intensity"])

        return cyclone_db_obj
