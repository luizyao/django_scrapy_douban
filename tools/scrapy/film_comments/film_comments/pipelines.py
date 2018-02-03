# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import sqlite3
import logging
from scrapy.exceptions import DropItem 
from datetime import datetime 

class FilmCommentsPipeline(object):
    def open_spider(self, spider):
        pass
    
    def process_item(self, item, spider):
        pass  

    def close_spider(self, spider):
        pass 
