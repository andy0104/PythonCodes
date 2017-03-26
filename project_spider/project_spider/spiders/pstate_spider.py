import scrapy

class PstateSpider(scrapy.Spider):
    name = 'pstate'

    def start_requests(self):
        start_urls = ['http://publicrecords.onlinesearches.com/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_state)

    def parse_state(self, response):
        state_list = []
        state_id = 0
        i = 0

        for tag in response.css('ul.grid__item li'):
            state_url = str(tag.css('a::attr(href)').extract_first().strip())

            if state_url is not None:
                state_url = response.urljoin(state_url)

            state_id += 1
            county_list = []
            #county_list = yield scrapy.Request(url=state_url, callback=self.parse_county)

            state_name = str(tag.css('a::text').extract_first().strip())

            yield {
                'id': state_id,
                'state_name': str(tag.css('a::text').extract_first().strip()),
                #'state_url': str(tag.css('a::attr(href)').extract_first().strip())
                'state_url': state_url,
                'counties': county_list
            }
