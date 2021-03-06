# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .bookfeed import BookFeed


class JinyongPipeline(object):
    def open_spider(self, spider):
        self.books = BookFeed()

    def process_item(self, item, spider):
        self.books.feed(item)
        return item

    def close_spider(self, spider):
        self.books.getAllBooks1PDF()
