# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PchomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    class_num = scrapy.Field()
    class_no = scrapy.Field()
    no = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    original_price = scrapy.Field()
    images = scrapy.Field()

class BeForm(scrapy.Item):
    pass