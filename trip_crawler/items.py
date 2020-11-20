# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripCrawlerItem(scrapy.Item):
    page = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()


class MafengwoItem(scrapy.Item):
    page = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
