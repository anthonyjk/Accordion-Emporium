import scrapy
from scrapy.crawler import CrawlerProcess

# on CMD:
# scrapy crawl alamo

class LibertySpider(scrapy.Spider):
    name = 'liberty'
    start_urls = ['https://www.libertybellows.com/shop/Piano-Accordions.htm?pageNum=1']

   # response.css('div.cItemDiv a::attr(href)')
   # pages = response.css('div.col-lg-4.col-md-6.col-sm-12.col-xs-12.align-center-between a::attr(href)').get()

    def parse(self, response):
        #price = response.css('p.cItemPrice::text').get()

        for link in response.css('div.cItemDiv a::attr(href)'):
            yield response.follow(link.get(), callback=self.page_crawl)

    def page_crawl(self, response):
       information = response.css('p#prod_description::text')
       data = []
       for info in information:
          data.append(info.get())

       print(data)

       yield {
            'info': data
        }

class AlamoSpider(scrapy.Spider):
    name = 'alamo'
    start_urls = ['https://www.alamomusic.com/collections/accordions?page=1&grid_list=grid-view']

    def parse(self, response):
        for products in response.css('div.productitem--info'):
            yield {
                'name' : products.css('h2.productitem--title > a::text').get().replace('  ', '').replace('\n', ''),
                'price' : products.css('span.money::text').get().replace(' ', '').replace('\n', '').replace("$", '').replace(",", ""),
                'link' : products.css('a').attrib['href'],
            }

        next_page = response.css('a.pagination--item').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

def crawl_to_json():
    settings = {
            'FEEDS': {
                    'accordion.json': {
                        'format': 'json',
                        'overwrite': True
                    }
            },
            'LOG_LEVEL': 'INFO'
    }
    process = CrawlerProcess(settings)

    process.crawl(AlamoSpider)
    process.start()
