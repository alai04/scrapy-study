# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jinyongwang.com']
    start_urls = ['http://www.jinyongwang.com/book/']

    def parse(self, response):
        # //p[@class='title']/a[starts-with(@href, '/n')]   新修版
        for link in response.xpath("//p[@class='title']/a[starts-with(@href, '/n')]/@href").extract():
            yield scrapy.Request(response.urljoin(link), callback=self.book_parse)

    def book_parse(self, response):
        # //h1[@class='title']/span/text()         Book name
        # //ul[@class='mlist']/li/a                Chapter link
        for link in response.xpath("//ul[@class='mlist']/li/a/@href").extract():
            yield scrapy.Request(response.urljoin(link), callback=self.chap_parse)

    def chap_parse(self, response):
        # //div[@class='topleft']/span/a/text()     Book name
        # //h1[@id='title']/text()      Chapter name
        # //div[@id='vcon']/p/text()    Content
        yield {
            'sn': response.url.split('/')[-1].split('.')[0],
            'book': response.xpath("//div[@class='topleft']/span/a/text()").extract()[1],
            'chap': response.xpath("//h1[@id='title']/text()").extract_first(),
            'lines': response.xpath("//div[@id='vcon']/p/text()").extract(),
        }
