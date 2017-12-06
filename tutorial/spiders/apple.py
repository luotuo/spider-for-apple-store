#! usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import TutorialItem
from urllib import unquote
import re


class AppleSpider(scrapy.Spider):
    name = 'apple'
    allowed_domains = ['itunes.apple.com']
    current_category = {}

    def start_requests(self):
        yield scrapy.Request('https://itunes.apple.com/cn/genre/ios/id36?mt=8', self.parse)

    def parse(self, response):
        my_item = TutorialItem()
        app_url = response.url
        app_name = response.xpath('//h1[@itemprop="name"]/text()').extract()
        if len(app_name) > 0:
            category = response.meta['category']
            my_item['app_name'] = app_name[0]
            app_category = response.xpath('//span[@itemprop="applicationCategory"]/text()').extract()
            if len(app_category) > 0:
                my_item['app_category'] = category[0]
            content = response.xpath('//p[@itemprop="description"]/text()').extract()
            temp_content = ""
            if len(content) > 0:
                for c in content:
                    temp_content += c
                my_item['app_content'] = temp_content
                if my_item['app_category'] in self.current_category:
                    self.current_category[my_item['app_category']] += 1
                else:
                    self.current_category[my_item['app_category']] = 1

                my_item['app_rank'] = self.current_category[my_item['app_category']]
                my_item['app_url'] = app_url
                my_item['app_developer'] = response.xpath('//div[@class="left"]//h2/text()').extract()[0]
        yield my_item
        decode_url = unquote(app_url)
        category = re.findall(r"https://itunes.apple.com/cn/genre/ios-(.*)/.*?", decode_url)

        for url in response.xpath('//div[@class="grid3-column"]//ul//li//a/@href').extract():
            yield scrapy.Request(url, meta={'category':category}, callback=self.parse)

