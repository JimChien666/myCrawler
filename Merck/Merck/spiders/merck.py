# -*- coding: utf-8 -*-
import scrapy
import pymysql
from Merck import settings
import json
from Merck.items import MerckItem
from copy import deepcopy

class MerckSpider(scrapy.Spider):
    name = 'merck'
    allowed_domains = ['merckmillipore.com']
    # start_urls = ['http://merckmillipore.com/']

    def start_requests(self):
        url = 'https://www.merckmillipore.com/INTL/en'
        yield scrapy.Request(
            url,
            callback=self.parse_en
        )

    def parse_en(self, response):
        url = "https://www.merckmillipore.com/TW/zh"
        yield scrapy.Request(
            url,
            callback=self.parse_home,
            dont_filter=True
        )

    def parse_home(self, response):
        login = pymysql.connect(
            host=settings.host,
            port=settings.port,
            user=settings.user,
            passwd=settings.passwd,
            db=settings.db)
        c = login.cursor()
        cmd = 'SELECT p.id, vpr.vendor_product_no, psf.content FROM products p left join vendor_product_refs vpr on p.id = vpr.product_id left join product_spec_refs psf on p.id = psf.product_id where vpr.vendor_id = 406 and psf.product_spec_id = 1006'
        c.execute(cmd)
        datas = c.fetchall()
        c.close()
        for data in datas:
            items = MerckItem()
            items['product_id'] = data[0]
            product_url = f"https://www.merckmillipore.com/Web-TW-Site/zh_TW/-/TWD/GetERPProductPrice-Start?ProductSKU={data[2].split(',')[-1].split('-')[0]}-{data[1].replace('.', '')}&Quantity=1&PageType=PDP_PFP_SERP&ProductType=QTY"
            yield scrapy.Request(
                product_url,
                callback=self.parse_stock,
                meta={'items': deepcopy(items)}
            )

    def parse_stock(self, response):
        items = response.meta['items']
        js = json.loads(response.body.decode())
        if js.get('availArray'):
            items['stock_status'] = js.get('availArray')
        else:
            items['stock_status'] = None
        yield items