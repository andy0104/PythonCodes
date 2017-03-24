import scrapy
import MySQLdb
import urllib2

# Open database connection
#db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler', unix_socket = '/opt/lampp/var/mysql/mysql.sock')

# prepare a cursor object using cursor() method
cursor = db.cursor()

class PlinksSpider(scrapy.Spider):
    name = "plinks"
    state_id = 0
    # custom_settings = {
    #     #"DOWNLOAD_DELAY": 5,
    #     "CONCURRENT_REQUESTS_PER_DOMAIN": 5
    # }

    def start_requests(self):
        start_urls = ['http://publicrecords.onlinesearches.com/']

        sql = 'TRUNCATE TABLE state_links'

        try:
           # Execute the SQL command
           cursor.execute(sql)

           # Commit your changes in the database
           db.commit()

        except:
           # Rollback in case there is any error
           print 'State_links trucnate failed'
           db.rollback()

        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM state ORDER BY id"

        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            for state in result:
                state_url = state[2]
                self.state_id = state[0]

                yield scrapy.Request(url=state_url, callback=self.parse_state)

        except:
            print "State url not matched"

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'public-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse_state(self, response):
        state_list = []
        i = 0

        st_id = 0

        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM state WHERE \
               state_url = '%s'" % \
               (response.url)

        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            st_id = result[0]
        except:
            print "State url not matched"

        #county_links = yield scrapy.Request(url=response.url, callback=self.start_county)
        final_url_reached = '0'

        for tag in response.css('table.results-list tr'):
            tmp_url = ''
            link_url = str(tag.css('td.regular-link-div a::attr(href)').extract_first())
            if link_url is not None:
                link_url = response.urljoin(link_url)
                tmp_url = link_url
                print tmp_url
                #var = urllib2.urlopen(link_url)
                #print var.geturl()
                #link_url = var.geturl()
                #link_url = urllib2.urlopen(link_url, None, 1).geturl()
                link_url = self.get_final_url(link_url)

                if tmp_url != link_url:
                    final_url_reached = '1'
                else:
                    final_url_reached = '0'
            else:
                link_url = ''

            link_title = tag.css('td.regular-link-div a::text').extract_first()
            if link_title is not None:
                link_title = str(tag.css('td.regular-link-div a::text').extract_first().strip())
            else:
                link_title = ''

            link_desc = tag.css('td.regular-link-div div.desc::text').extract_first()
            if link_desc is not None:
                link_desc = str(tag.css('td.regular-link-div div.desc::text').extract_first().encode('utf-8').strip())
            else:
                link_desc = ''

            link_type = tag.css('td.record-type div.record-label::text').extract_first()
            if link_type is not None:
                link_type = str(tag.css('td.record-type div.record-label::text').extract_first())

            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO state_links(state_id, link_title, link_url, link_desc, link_type, final_url_reached) \
                   VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                   (st_id, link_title, link_url, link_desc, link_type, final_url_reached)

            try:
               # Execute the SQL command
               cursor.execute(sql)

               #Get last insert id
               self.state_link_id = cursor.lastrowid

               # Commit your changes in the database
               db.commit()

            except:
               # Rollback in case there is any error
               db.rollback()

            yield {
                'state_id': st_id,
                'link_title': link_title,
                #'state_url': str(tag.css('a::attr(href)').extract_first().strip())
                'link_url': link_url,
                'link_desc': link_desc,
                'link_type': link_type,
                'headers': response.headers
            }

    def spider_closed(self, spider):
        print "Spider Finished!!"
        spider.logger.info('Spider closed: %s', spider.name)
        db.close()

    def get_final_url(self, link_url):
        try:
            link_url = urllib2.urlopen(link_url, None, 1).geturl()
        except:
            print "Could not get final url"

        return link_url
