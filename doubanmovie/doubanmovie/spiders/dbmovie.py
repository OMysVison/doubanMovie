# -*- coding: utf-8 -*-
import scrapy
import re
from doubanmovie.items import DoubanmovieItem

class DbmovieSpider(scrapy.Spider):
    name = 'dbmovie'
    # allowed_domains = ['https://www.douban.com/doulist/107486/']
    start_urls = ['https://www.douban.com/doulist/107486/']

    def parse(self, response):
        item = DoubanmovieItem()
        selector = scrapy.Selector(response)
        movies = selector.xpath('//div[@class="bd doulist-subject"]')
        for each in movies:
            title = each.xpath('div[@class="title"]/a/text()').extract()[0]
            rate = each.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
            director = re.search('<div class="abstract">(.*?)<br',each.extract(),re.S).group(1)
            img = each.xpath('div[@class="post"]/a/img/@src').extract()[0]
            item['title'] = title
            item['rate'] = rate
            item['director'] = director
            item['img'] = img
        	     
            yield item
            nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:
                nextSelector = nextPage[0]
                yield scrapy.http.Request(nextSelector,callback=self.parse)
