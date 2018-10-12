"""
    This is the spider file.
    This file requests the allowed url and keeps on searching till getting callbacks,
    for the filtered items.
    - Sumit Singh Kanwal
"""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import CycloneForecast, Cyclone, CycloneTrackHistory, ForecastTrack


class CycloneSpider(CrawlSpider):
    """
        This is the spider class.
        This scrapy spider will get all the cyclone information and parse it to the,
        scrapy items.
    """
    name = "cyclone"
    allowed_domains = ['rammb.cira.colostate.edu']
    start_urls = ['http://rammb.cira.colostate.edu/products/tc_realtime/index.asp']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=(['//div[@class="basin_storms"]/ul/li/a'])),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):

        """
            @url http://rammb.cira.colostate.edu/products/tc_realtime/index.asp
            @returns items 0 2
            @returns requests 0 0
            @scrapes name
            """

        cyclone_name = response.css('h2::text').extract()
        cyclone_obj = Cyclone()
        cyclone_obj['name'] = cyclone_name

        yield cyclone_obj

        time_of_latest_forcast = response.css('.text_product_wrapper > h4::text').extract()
        cyclone_forecast_obj = CycloneForecast(cyclone_obj)
        cyclone_forecast_obj['time_of_forecast'] = time_of_latest_forcast

        yield cyclone_forecast_obj

        if len(response.css('table').extract()) > 2:

            forcast_track = response.css('table')[0].css('td::text').extract()

            for i in range(4, len(forcast_track), 4):
                forcast_track_obj = ForecastTrack(cyclone_forecast_obj)

                forcast_track_obj['forecast_hour'] = forcast_track[i]
                forcast_track_obj['latitude'] = forcast_track[i+1]
                forcast_track_obj['longitude'] = forcast_track[i+2]
                forcast_track_obj['intensity'] = forcast_track[i+3]

                yield forcast_track_obj

            cyclone_track_history = response.css('table')[1].css('td::text').extract()
            for j in range(4, len(cyclone_track_history), 4):
                cyclone_track_history_obj = CycloneTrackHistory(cyclone_obj)

                cyclone_track_history_obj['synoptic_time'] = cyclone_track_history[j]
                cyclone_track_history_obj['latitude'] = cyclone_track_history[j+1]
                cyclone_track_history_obj['longitude'] = cyclone_track_history[j+2]
                cyclone_track_history_obj['intensity'] = cyclone_track_history[j+3]

                yield cyclone_track_history_obj
