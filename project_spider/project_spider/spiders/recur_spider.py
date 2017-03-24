import scrapy

class RecurSpider(scrapy.Spider):
    #this name has to match the file name (minus spider)
    name = 'recur'

    def start_requests(self):
        urls = ['http://quotes.toscrape.com/page/1/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        #Getting the next link
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None: #Checking if link exist or not
            #creatign a traversable link
            next_page = response.urljoin(next_page)
            #calling the scrapy parse method on next link
            #calling the link recursively until no next link
            yield scrapy.Request(next_page, callback=self.parse)
