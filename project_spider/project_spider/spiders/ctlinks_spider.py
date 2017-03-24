import scrapy
import MySQLdb
import urllib2

# Open database connection
#db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler', unix_socket = '/opt/lampp/var/mysql/mysql.sock')

# prepare a cursor object using cursor() method
cursor = db.cursor()

class CtlinksSpider(scrapy.Spider):
    name = "ctlinks"
    state_id = 0
    handle_httpstatus_all = True
    # custom_settings = {
    #     "DOWNLOAD_DELAY": 5,
    #     "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    # }

    def start_requests(self):
        start_urls = ['http://publicrecords.onlinesearches.com/']

        sql = 'TRUNCATE TABLE city_links'

        try:
           # Execute the SQL command
           cursor.execute(sql)

           # Commit your changes in the database
           db.commit()

        except:
           # Rollback in case there is any error
           print 'City_links trucnate failed'
           db.rollback()

        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM city ORDER BY id"

        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            for city in result:
                tmp_url = city[4]
                #city_url = city[4]
                city_url = tmp_url.split("#")[0]
                city_url = city_url.replace (" ","%20")
                city_url = city_url + 'l'
                self.city_id = city[0]

                yield scrapy.Request(url=city_url, callback=self.parse_city)
        except:
            print "City url not matched"

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'public-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse_city(self, response):
        county_list = []
        i = 0

        ct_id = 0
        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM city WHERE \
               city_url LIKE '%s'" % \
               (response.url + '%')
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            ct_id = result[0]
        except:
            print "City url not matched"

        link_title = ''
        link_url = ''
        link_desc = ''
        link_type = ''

        print 'Response: ' + response.css('table.results-list tr')[0].extract()

        for tag in response.css('table.results-list tr'):

            link_url = str(tag.css('td a::attr(href)').extract_first())
            if link_url is not None:
                link_url = response.urljoin(link_url)
                link_url = self.get_final_url(link_url)
            else:
                link_url = ''

            link_title = tag.css('td.regular-link-div a::text').extract_first()
            if link_title is not None:
                #link_title = str(tag.css('td.regular-link-div a::text').extract_first().encode('utf-8').strip())
                link_title = str(tag.css('td.regular-link-div a::text').extract_first())
            else:
                link_title = ''

            link_desc = tag.css('td.regular-link-div div.desc::text').extract_first()
            if link_desc is not None:
                link_desc = str(tag.css('td.regular-link-div div.desc::text').extract_first().encode('utf-8').strip())
            else:
                link_desc = ''

            link_type = tag.css('td div.record-label::text').extract_first()
            if link_type is not None:
                link_type = str(tag.css('td.record-type div.record-label::text').extract_first())
            else:
                link_type = ''

            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO city_links(city_id, link_title, link_url, link_desc, link_type) \
                   VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                   (ct_id, link_title, link_url, link_desc, link_type)
            print "Executing...."

            try:
               # Execute the SQL command
               cursor.execute(sql)

               #Get last insert id
               self.city_link_id = cursor.lastrowid

               # Commit your changes in the database
               db.commit()

            except:
               # Rollback in case there is any error
               print "City links insert error"
               db.rollback()

            yield {
                'response_url': response.url,
                'city_id': ct_id,
                'link_title': link_title,
                'link_url': link_url,
                'link_desc': link_desc,
                'link_type': link_type
            }

    def spider_closed(self, spider):
        print "Spider Finished!!"
        spider.logger.info('Spider closed: %s', spider.name)
        db.close()

    def get_final_url(self, link_url):
        try:
            link_url = urllib2.urlopen(link_url, None, 1).geturl()
        except urllib2.URLError as e:
            print "N F: " + link_url
            print "Could not get final url"
            print e.reason

        return link_url
