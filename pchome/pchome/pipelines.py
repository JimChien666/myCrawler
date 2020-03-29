# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
# from .items import PchomeItem

class PchomePipeline(object):
    def process_item(self, item, spider):
        return item


class PchomeImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(
                image_url,
                meta={'no': item['no']}
            )
    def file_path(self, request, response=None, info=None):
        name = request.meta['no']

        return f"{name}.jpg"

class PchomeContentImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for content_pic_url in item['content_pic_urls']:
            yield Request(
                content_pic_url
            )
    def file_path(self, request, response=None, info=None):
        file_name = request.url.split("/")[-2]
        name = request.url.split("/")[-1]

        return f"{file_name}/{name}"