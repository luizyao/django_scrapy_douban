# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmCommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cus_name = scrapy.Field()
    comment = scrapy.Field()
    grade = scrapy.Field()
    time = scrapy.Field()
    film_name = scrapy.Field()
    source = scrapy.Field()
