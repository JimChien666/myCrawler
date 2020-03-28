# -*- coding: utf-8 -*-
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile/']

    def parse(self, response):
        key = response.css('table label::text').re('(.+):')
        value = response.css("table td.w2p_fw::text").extract()

        yield dict(zip(key, value))


    # 登入----------------------------------------
    login_url = 'http://example.webscraping.com/places/default/user/login'
    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)
    def login(self, response):
        fd = {'email': "shit18754678@gmail.com", 'password': 'X93nfnane4UQpAc'}
        yield scrapy.FormRequest.from_response(response, formdata=fd, callback=self.parse_login)
    def parse_login(self, response):
        if 'Welcome' in response.text:
            yield from super().start_requests()