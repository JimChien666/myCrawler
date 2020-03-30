# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PchomeItem(scrapy.Item):
    class_num = scrapy.Field()
    no = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    original_price = scrapy.Field()
    images = scrapy.Field()
    content_pic_urls = scrapy.Field()
    content_pic = scrapy.Field()
    spec = scrapy.Field()

class BeForm(scrapy.Item):
    pass