"""
    This is the Scrapy Item file.
    The crawled data is stored in the Scrapy Item object.
    This is more of unstructured data compared to models file. Hence just the Field.
    - Sumit Singh Kanwal
"""

import scrapy


class Cyclone(scrapy.Item):
    """
        This is the Cyclone Scrapy Item file.
    """
    name = scrapy.Field()


class CycloneForecast(Cyclone):
    """
        This is the CycloneForecast Scrapy Item file.
    """
    time_of_forecast = scrapy.Field()


class CycloneTrackHistory(Cyclone):
    """
        This is the CycloneTrackHistory Scrapy Item file.
    """
    synoptic_time = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    intensity = scrapy.Field()


class ForecastTrack(CycloneForecast):
    """
        This is the ForecastTrack Scrapy Item file.
    """
    forecast_hour = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    intensity = scrapy.Field()
