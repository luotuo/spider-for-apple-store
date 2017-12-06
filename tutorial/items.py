# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    app_name = scrapy.Field()
    app_category = scrapy.Field()
    app_rank = scrapy.Field()
    app_content = scrapy.Field()
    app_url = scrapy.Field()
    app_developer = scrapy.Field()