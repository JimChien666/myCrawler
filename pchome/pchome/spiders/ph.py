# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
from pchome.settings import ALL_CLASS
from pchome.items import PchomeItem
import json


class PhSpider(scrapy.Spider):
    name = 'ph'
    # allowed_domains = ['ecapi.pchome.com.tw', 'mall.pchome.com.tw']
    # start_urls = [
    #     f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{class_}/prod&offset=0&limit=30&fields=Id,Nick,Pic,Price,Discount,isSpec,Name,isCarrier,isSnapUp,isBigCart,isPrimeOnly,isETicket&_callback=top_prod?_callback=top_prod'
    #     for class_ in ALL_CLASS]

    def start_requests(self):
        for class_ in ALL_CLASS:
            item = PchomeItem()
            start_num = 0
            item['class_num'] = ALL_CLASS[class_]['class_num']
            url = f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{class_}/prod&offset={start_num}&limit=30&fields=Id&_callback=top_prod?_callback=top_prod'
            yield scrapy.Request(
                url,
                meta={"item": deepcopy(item), "class_": deepcopy(class_)},
                callback=self.parse,
                dont_filter=True
            )



    def parse(self, response):
        item = response.meta['item']
        start_num = 0
        class_ = response.meta['class_']
        limit = 30
        if response.text != 'try{top_prod([]);}catch(e){if(window.console){console.log(e);}}':
            res_content = re.compile(r"try{top_prod\((.+)\);}catch\(e\)")
            product_str = res_content.search(response.body.decode('utf-8')).group(1)
            products = json.loads(product_str)
            for product in products:
                item['no'] = re.sub('-000', '', product['Id'])
                product_url = f"https://mall.pchome.com.tw/ecapi/ecshop/prodapi/v2/prod/{product['Id']}&store={class_}&fields=Nick,Price,Pic,Qty&_callback=jsonp_prod&1585406880?_callback=jsonp_prod"
                yield scrapy.Request(
                    product_url,
                    meta={"item": deepcopy(item), "class_": deepcopy(class_)},
                    headers={'Referer': f'https://mall.pchome.com.tw/prod/{product["Id"]}M?q=/S/{class_}'},
                    callback=self.parse_data_detail,
                    dont_filter=True
                )


            start_num = start_num + limit
            url = f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/{class_}/prod&offset={start_num}&limit={limit}&fields=Id&_callback=top_prod?_callback=top_prod'
            yield scrapy.Request(
                url,
                meta={"item": item, "start_num": start_num, "class_": class_},
                callback=self.parse,
                dont_filter=True
            )
    def parse_data_detail(self, response):
        item = response.meta['item']
        class_ = response.meta['class_']
        res_content = re.compile(r"try{jsonp_prod\((.+)\);}catch\(e\)")
        product_str = res_content.search(response.body.decode('utf-8')).group(1)
        # print(product_str)
        product = json.loads(product_str)
        product = product.get(f"{item['no']}-000")
        item['name'] = product['Nick']
        item['price'] = product['Price']['P']
        item['original_price'] = product['Price']['M']
        item['image_urls'] = [f"https://d.ecimg.tw/{product['Pic']['B']}"]
        content_pic_js_url = f"https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/{item['no']}/intro&fields=Pic&_callback=jsonp_intro?_callback=jsonp_intro"
        yield scrapy.Request(
            content_pic_js_url,
            headers={'Referer': f"https://mall.pchome.com.tw/prod/{item['no']}?q=/S/QAAI0D"},
            meta={"item": item, "class_": class_},
            callback=self.parse_pic_js,
            dont_filter=True
        )

    def parse_pic_js(self, response):
        item = response.meta['item']
        class_ = response.meta['class_']
        res_content_pics_js = re.compile(r"try{jsonp_intro\((.+)\);}catch\(e\)")
        content_pics_js = res_content_pics_js.search(response.body.decode('utf-8')).group(1)
        content_pics = json.loads(content_pics_js)
        item['content_pic_urls'] = [f"https://e.ecimg.tw{pic['Pic']}" for pic in list(content_pics.values())[0]]
        yield item


