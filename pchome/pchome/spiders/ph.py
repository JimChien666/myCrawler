# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
import urllib
from pchome.settings import ALL_CLASS
from pchome.items import PchomeItem
import json


class PhSpider(scrapy.Spider):
    name = 'ph'
    allowed_domains = ['ecapi.pchome.com.tw']
    # start_urls = [
    #     f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{class_}/prod&offset=0&limit=30&fields=Id,Nick,Pic,Price,Discount,isSpec,Name,isCarrier,isSnapUp,isBigCart,isPrimeOnly,isETicket&_callback=top_prod?_callback=top_prod'
    #     for class_ in ALL_CLASS]

    def start_requests(self):
        for class_ in ALL_CLASS:
            item = {}
            limit = 30
            start_num = 0
            item["start_num"] = start_num
            item["class_"] = class_
            url = f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{class_}/prod&offset={start_num}&limit={limit}&fields=Id&_callback=top_prod?_callback=top_prod'
            yield scrapy.Request(
                url,
                meta={"item": item},
                callback=self.parse,
                dont_filter=True
            )



    def parse(self, response):
        item = response.meta['item']
        data = PchomeItem()
        data['class_num'] = ALL_CLASS[item["class_"]]['class_num']
        data['class_no'] = item["class_"]
        limit = 30
        if response.text != 'try{top_prod([]);}catch(e){if(window.console){console.log(e);}}':
            products = response.body.decode('utf-8').replace('try{top_prod(', '').replace(
                ');}catch(e){if(window.console){console.log(e);}}', '')
            products = json.loads(products)
            for product in products:
                data['no'] = product['Id']
                product_url = f"https://mall.pchome.com.tw/ecapi/ecshop/prodapi/v2/prod/{product['Id']}&store={data['class_no']}&fields=Id,Nick,Price,Pic,Qty&_callback=jsonp_prod&1583813520?_callback=jsonp_prod"
                yield scrapy.Request(
                    product_url,
                    meta={'data': data},
                    callback=self.parse_data_detail,
                    dont_filter=True
                )


            item["start_num"] = item['start_num'] + limit
            url = f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{item["class_"]}/prod&offset={item["start_num"]}&limit={limit}&fields=Id&_callback=top_prod?_callback=top_prod'
            yield scrapy.Request(
                url,
                meta={"item": item},
                callback=self.parse,
                dont_filter=True
            )

    def parse_data_detail(self, response):
        data = response.meta['data']
        products = response.body.decode('utf-8')
        print(products)