import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.miga-restaurant.com/menu.html"
    ]

    def parse(self, response):

        # sel = Selector(response)
        # sites = s
        items = []
        fp = open('result.json','w')
        fp.write('{ "menu": {\n\t "menuItems" :[ \n\t\t \r')

        for site in Selector(response).xpath('//ul[@class="menu-list"]/li'):
            item = Website()
            item['name'] = site.xpath('p[@class="menu-title"]/text()').extract()
            item['descrip'] = site.xpath('p[@class="menu-desc"]/text()').extract()
            # item['category'] = 'null'
            item['price'] = site.xpath('p[@class="menu-price"]/text()').extract()
            items.append(item)

            s = str(items) + ','   
            yield items 
            fp.write(s + '\r'+ '\r')
              


        fp.write(']' + '\r' + '}' '\r' + '}')


            
  

