# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem

class TencentpositionSpider(scrapy.Spider):
    name = 'tencentPosition'
    allowed_domains = ['tencent.com']
    url = 'http://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        for each in response.xpath("//tr[@class = 'even'] | //tr[@class = 'old']"):
            item = TencentItem()
            # 职位名称
            item['positionname'] = each.xpath('./td[1]/a/text()').extract()[0]
            # 详情链接
            item['positionlink'] = each.xpath('./td[1]/a/@href').extract()[0]
            # 职位类别
            try:
                item['postiontype'] = each.xpath('./td[2]/text()').extract()[0].split()

            except Exception as e:
                pass
            else:
                pass


            # 招聘人数
            item['peopleNum'] = each.xpath('./td[3]/text()').extract()[0]
            # 发布时间
            item['publishTime'] = each.xpath('./td[5]/text()').extract()[0]
            # 工作地点
            item['workplace'] = each.xpath('./td[4]/text()').extract()[0]
            yield item


        if self.offset < 3510:
            self.offset += 10

        # 每次处理完一页的数据之后，重新发送下一页页面请求
        # self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

            # 将数据发送到管道文件

