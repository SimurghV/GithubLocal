# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class Vmgscrapyv2Pipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['article_name']
        image_guid = request.url.split('/')[-1]
        filename = u'VMgirls/{0}/{1}'.format(folder, image_guid)
        return filename

    def get_media_requests(self, item, info):
        for img_url in item['img_urls']:
            referer = item['article_url']
            yield Request(img_url, meta={'item': item, 'referer': referer})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Itme contains no images")
        return item


if __name__ == "__main__":
    a = 'This is a wrong character'
    print(a)
