# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Vmgscrapyv2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_name = scrapy.Field()
    article_url = scrapy.Field()
    img_urls = scrapy.Field()
    article_counter = scrapy.Field()
    pass
