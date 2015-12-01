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
        fp.write('{ "menu": {\n\t"menuItems" :[ \n\t\t \r')

        for site in Selector(response).xpath('//ul[@class="menu-list"]/li'):
            item = Website()
            item['name'] = site.xpath('p[@class="menu-title"]/text()').extract()
            item['description'] = site.xpath('p[@class="menu-desc"]/text()').extract()
            item['category'] = site.xpath('//h3[@class="primary-title"]/img/@alt').extract()
            item['price'] = site.xpath('p[@class="menu-price"]/text()').extract()
            items.append(item)

            fp.write('\t\t{ \r \t\t\t"name": "' + item['name'][0] + '", \r')
            fp.write('\t\t\t"description": "' + item['description'][0] + '", \r') 
            fp.write('\t\t\t"category": "' + item['category'][0] + '", \r') 
            # fp.write(item['category'][0]) 
            fp.write('\t\t\t"price": "' + item['price'][0] + '" \r\t\t},\n') 
            print item['category'][0]
        # s = str(items) + ','   
        # yield items 
        # fp.write(s + '\r'+ '\r')
              


        fp.write('\t]' + '\r\t\t' + '}' '\r' + '}')


            
  

