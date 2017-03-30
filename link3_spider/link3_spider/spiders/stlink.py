# -*- coding: utf-8 -*-
import scrapy
import MySQLdb

try:
    # Open database connection
    #db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
    db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler_1', unix_socket = '/opt/lampp/var/mysql/mysql.sock')
    print "Db connected"
except:
    print "Db not connected"

try:
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    print "Cursor created"
except:
    print "Cannot create cursor"

class StlinkSpider(scrapy.Spider):
    name = "stlink"
    #allowed_domains = ["example.com"]
    #start_urls = ['http://example.com/']

    def start_requests(self):
        
    	sql_state = "SELECT id, state_name, state_url FROM state ORDER BY id ASC"

    	try:
    		cursor.execute(sql_state)
    		result = cursor.fetchall()

    		for row in result:
    			state_url = row[2]

    			try:
    				yield scrapy.Request(url=state_url, callback=self.parse)
    			except:
    				print "Error fetching url"

    	except Exception as e:
    		print "Error getting sate urls ", e

    def parse(self, response):
        
        st_id = 0
    	sql_state = "SELECT id FROM state WHERE state_url = '%s' " % (response.url)

    	try:
    		cursor.execute(sql_state)
    		row = cursor.fetchone()
    		st_id = row[0]
    	except Exception as e:
    		print "Error fetching state with url ", e

        for tag in response.css('div.panel-body ul.content_directory li'):
        	link_url = str(tag.css('h4 a::text').extract_first().strip())
        	link_title = str(tag.css('h4 a::attr(href)').extract_first().strip())
        	link_desc = str(tag.css('span::text').extract_first().strip())
        	
        	sql_ins = "INSERT INTO state_links(state_id, link_title, link_url, link_desc, final_url_reached) \
        				VALUES('%s', '%s', '%s', '%s', '%s') " % (st_id, link_title, link_url, link_desc, '1')

        	try:
        		cursor.execute(sql_ins)
        		db.commit()
        	except Exception as e:
        		db.rollback()
        		print "Error inserting data to state links table ", e

        	yield {
        		'state_id': st_id,
        		'link_title': link_title,
        		'link_desc': link_desc,
        		'link_url': link_url
        	}
