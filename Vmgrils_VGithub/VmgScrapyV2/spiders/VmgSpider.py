"""
Created on 25JN18
By: SimurghV

Created on python3.6.5
Target: http://www.vmgirls.com
a purity girl pictures website, not all resoures, only in articles.

set store path in setting.py
and run start.py

Got a problem?  Ask me!

If U like it, welcome donate(BTC):
1NSHvb9VNb6Zsp6HTcS1SLuWxwyQ4TtHSB
or if U enjoy those beautiful picture, please support that website.

HAGD!
"""

from VmgScrapyV2.items import Vmgscrapyv2Item
import re
from scrapy import Request
import scrapy
from scrapy import Spider


class VSpider(Spider):
    name = 'Vmgscrapyv2'
    article_counter = 0
    allow_domains = ['www.vmgirls.com']
    Download_pages_num = 1000  # how many page to download

    def start_requests(self):
        return [scrapy.FormRequest("http://www.vmgirls.com", callback=self.max_page)]

    # get max page number, and generate all pages url
    def max_page(self, response):
        maxpage_list = response.xpath(
            '//nav[@class="navigation pagination"]//a[@class="page-numbers"][last()]/text()').extract()
        maxpage = int(re.sub(r'[^0-9]', '', str(maxpage_list)))
        for page in range(maxpage):
            url = 'https://www.vmgirls.com/?paged='+str(page+1)+'&'
            if page+1 > self.Download_pages_num:
                break
            yield Request(url, callback=self.parse_page)

    # get article url
    def parse_page(self, response):
        artic_url = response.xpath('//ul[@class="update_area_lists cl"]/li[@class="i_list list_n2"]/a/@href').extract()
        for url in artic_url:
            yield Request(url, callback=self.parse_article)

    # get article name, url, and return item
    def parse_article(self, response):
        item = Vmgscrapyv2Item()
        img_urls = []  # temporary store all pictures' url

        article_name = response.xpath('//div[@class="main"]//div[@class="item_title"]/h1/text()').extract()
        # delete \u202a , come from html text：&#8234
        article_name_ua = re.sub(r'u202a', '', str(article_name))
        # delete（\u4e00-\u9fa5 A-Za-z 0-9 \s）
        item['article_name'] = re.sub(r'[^\u4e00-\u9fa5A-Za-z0-9\s]', '', str(article_name_ua))
        item['article_url'] = response.url
        self.article_counter += 1
        item['article_counter'] = self.article_counter

        imgurls_list = response.xpath('//div[@class="content_left"]//img/@src').extract()
        for imgurl in imgurls_list:
            img_urls.append(imgurl)
        item['img_urls'] = img_urls
        yield item
