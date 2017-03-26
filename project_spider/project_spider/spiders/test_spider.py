import scrapy
import MySQLdb

# Open database connection
#db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
#db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler', unix_socket = '/opt/lampp/var/mysql/mysql.sock')

# prepare a cursor object using cursor() method
#cursor = db.cursor()

class TestSpider(scrapy.Spider):
    name = "test"
    state_id = 0

    def start_requests(self):
        start_urls = ['http://publicrecords.onlinesearches.com/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_state)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'public-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse_state(self, response):
        state_list = []
        i = 0

        for tag in response.css('ul.grid__item li'):
            state_url = str(tag.css('a::attr(href)').extract_first().strip())

            if state_url is not None:
                state_url = response.urljoin(state_url)

            #self.state_id += 1
            county_list = []
            county_list = yield scrapy.Request(url=state_url, callback=self.parse_county)

            state_name = str(tag.css('a::text').extract_first().strip())

            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO state(state_name, state_url) \
                   VALUES ('%s', '%s')" % \
                   (state_name, state_url)

            # try:
            #    # Execute the SQL command
            #    cursor.execute(sql)
            #
            #    #Get last insert id
            #    self.state_id = cursor.lastrowid
            #
            #    # Commit your changes in the database
            #    db.commit()
            #
            # except:
            #    # Rollback in case there is any error
            #    db.rollback()

            yield {
                'id': self.state_id,
                'state_name': str(tag.css('a::text').extract_first().strip()),
                #'state_url': str(tag.css('a::attr(href)').extract_first().strip())
                'state_url': state_url,
                'counties': county_list
            }

    def parse_county(self, response):
        st_id = 0
        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM state WHERE \
               state_url = '%s'" % \
               (response.url)

        # try:
        #     cursor.execute(sql)
        #     result = cursor.fetchone()
        #     st_id = result[0]
        # except:
        #     print "State url not matched"

        county_list = []

        city_list = []

        for tag in response.css('ul.link-list li'):
            county_url = str(tag.css('a::attr(href)').extract_first().strip())

            if county_url is not None:
                county_url = response.urljoin(county_url)

            #Get all the city list for a county
            city_list = yield scrapy.Request(url=county_url, callback=self.parse_city)

            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO county(state_id, county_name, county_url) \
                   VALUES ('%s', '%s', '%s')" % \
                   (st_id, str(tag.css('a::text').extract_first().strip()), county_url)

            # try:
            #    # Execute the SQL command
            #    cursor.execute(sql)
            #
            #    #Get last insert id
            #    self.county_id = cursor.lastrowid
            #
            #    # Commit your changes in the database
            #    db.commit()
            #
            # except:
            #    # Rollback in case there is any error
            #    db.rollback()

            c_in = {
                'state_id': st_id,
                'county_name': str(tag.css('a::text').extract_first().strip()),
                'county_url': county_url
            }

            county_list.append(c_in)

        yield county_list

    def parse_city(self, response):

        county_id = 0
        county_state_id = 0
        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM county WHERE \
               county_url = '%s'" % \
               (response.url)

        # try:
        #     cursor.execute(sql)
        #     result = cursor.fetchone()
        #     county_id = result[0]
        #     county_state_id = result[1]
        # except:
        #     print "County url not matched"

        county_list = []
        for tag in response.css('ul.link-list li'):
            city_url = str(tag.css('a::attr(href)').extract_first().strip())

            if city_url is not None:
                city_url = response.urljoin(city_url)

            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO city(state_id, county_id, city_name, city_url) \
                   VALUES ('%s', '%s', '%s', '%s')" % \
                   (county_state_id, county_id, str(tag.css('a::text').extract_first().strip()), city_url)

            # try:
            #    # Execute the SQL command
            #    cursor.execute(sql)
            #
            #    #Get last insert id
            #    self.city_id = cursor.lastrowid
            #
            #    # Commit your changes in the database
            #    db.commit()
            #
            # except:
            #    # Rollback in case there is any error
            #    db.rollback()

            c_in = {
                'state_id': county_state_id,
                'county_id': county_id,
                'city_name': str(tag.css('a::text').extract_first().strip()),
                'city_url': city_url
            }

            county_list.append(c_in)

        return county_list

    def spider_closed(self, spider):
        print "Spider Finished!!"
        spider.logger.info('Spider closed: %s', spider.name)
        db.close()
