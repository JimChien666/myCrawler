# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Merck import settings
import time
from .items import MerckItem


class MerckPipeline(object):
    def __init__(self):
        # 1. 建立資料庫的連線
        self.connect = pymysql.connect(
            host=settings.host,
            port=settings.port,
            user=settings.user,
            passwd=settings.passwd,
            db=settings.db
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        updated_at = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if 'QTY_ON_EDD' in str(item['stock_status']):
            stocks = 1
            display_lead_time = '期貨3~5天'
        else:
            stocks = 0
            display_lead_time = '諮詢/訂購後通知'
        insert_sql = 'UPDATE vendor_product_refs SET `stocks` = "%s", `display_lead_time` = "%s", `updated_at` = "%s" where product_id = "%s";'% (stocks, display_lead_time, updated_at, item['product_id'])
        print(insert_sql)
        self.cursor.execute(insert_sql)
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
