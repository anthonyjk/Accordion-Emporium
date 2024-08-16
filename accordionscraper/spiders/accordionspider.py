import scrapy
from scrapy.crawler import CrawlerProcess

# on CMD:
# scrapy crawl accordion

class AccordionSpider(scrapy.Spider):
    name = 'accordion'
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

	process.crawl(AccordionSpider)
	process.start()
