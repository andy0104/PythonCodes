import scrapy
import MySQLdb
import urllib2

# Open database connection
#db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler', unix_socket = '/opt/lampp/var/mysql/mysql.sock')

# prepare a cursor object using cursor() method
cursor = db.cursor()

class ClinksSpider(scrapy.Spider):
    name = "clinks"
    state_id = 0
    # custom_settings = {
    #     "DOWNLOAD_DELAY": 5,
    #     "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    # }

    def start_requests(self):
        start_urls = ['http://publicrecords.onlinesearches.com/']

        sql = 'TRUNCATE TABLE county_links'

        try:
           # Execute the SQL command
           cursor.execute(sql)

           # Commit your changes in the database
           db.commit()

        except:
           # Rollback in case there is any error
           print 'County_links trucnate failed'
           db.rollback()

        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM county ORDER BY id"

        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            for county in result:
                county_url = county[3]
                self.county_id = county[0]

                yield scrapy.Request(url=county_url, callback=self.parse_county)

        except:
            print "County url not matched"

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'public-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse_county(self, response):
        county_list = []
        i = 0

        st_id = 0
        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM county WHERE \
               county_url = '%s'" % \
               (response.url)

        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            cn_id = result[0]
        except:
            print "County url not matched"

        county_name = str(response.css('section.county-info div.lap-and-up-two-thirds strong span.county-homepage::text').extract_first().strip())
        county_link = str(response.css('section.county-info div.lap-and-up-two-thirds strong a::attr(href)').extract_first().strip())
        if county_link is not None:
            county_link = response.urljoin(county_link)

        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO county_links(county_id, link_title, link_url, link_desc, link_type) \
               VALUES ('%s', '%s', '%s', '%s', '%s')" % \
               (cn_id, county_name, county_link, '', '')

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

        county_map_title = str(response.css('section.county-info div.lap-and-up-one-third figure figcaption a::text').extract_first().strip())
        county_map_link = str(response.css('section.county-info div.lap-and-up-one-third figure a::attr(href)').extract_first().strip())
        if county_map_link is not None:
            county_map_link = response.urljoin(county_map_link)

        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO county_links(county_id, link_title, link_url, link_desc, link_type) \
               VALUES ('%s', '%s', '%s', '%s', '%s')" % \
               (cn_id, county_map_title, county_map_link, '', '')

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

        final_url_reached = '0'

        for tag in response.css('table.results-list tr'):
            # For search link
            # search_link = str(tag.css('td.search-link-div a::attr(href)').extract_first())
            # if search_link is not None:
            #     search_link = response.urljoin(search_link)
            #
            #     search_title = tag.css('td.search-link-div a::text').extract_first()
            #     if search_title is not None:
            #         search_title = str(tag.css('td.search-link-div a::text').extract_first().strip())
            #     else:
            #         search_title = ''
            #
            #     search_desc = tag.css('td.search-link-div div.desc::text').extract_first()
            #     if search_desc is not None:
            #         search_desc = str(tag.css('td.search-link-div div.desc::text').extract_first().strip())
            #     else:
            #         search_desc = ''
            #
            #     search_type = ''
            #
            #     yield {
            #         'county_name': county_name,
            #         'county_link': county_link,
            #         'county_map_title': county_map_title,
            #         'county_map_link': county_map_link,
            #         'county_id': cn_id,
            #         'link_title': search_title,
            #         'link_url': search_link,
            #         'link_desc': search_desc,
            #         'link_type': search_type
            #     }

            link_url = str(tag.css('td.regular-link-div a::attr(href)').extract_first())
            if link_url is not None:
                link_url = response.urljoin(link_url)

                tmp_url = link_url
                print tmp_url

                link_url = self.get_final_url(link_url)

                if tmp_url != link_url:
                    final_url_reached = '1'
                else:
                    final_url_reached = '0'

                print 'Final url reached:' + final_url_reached
            else:
                link_url = ''

            link_title = tag.css('td.regular-link-div a::text').extract_first()
            if link_title is not None:
                link_title = str(tag.css('td.regular-link-div a::text').extract_first().encode('utf-8').strip())
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
            else:
                link_type = ''

            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO county_links(county_id, link_title, link_url, link_desc, link_type, final_url_reached) \
                   VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                   (cn_id, link_title, link_url, link_desc, link_type, final_url_reached)

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
                'county_name': county_name,
                'county_link': county_link,
                'county_map_title': county_map_title,
                'county_map_link': county_map_link,
                'county_id': cn_id,
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
