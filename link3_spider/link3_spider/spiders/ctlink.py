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

class CtlinkSpider(scrapy.Spider):
    name = "ctlink"
    #allowed_domains = ["example.com"]
    #start_urls = ['http://example.com/']

    def start_requests(self):
    	sql_truc = "TRUNCATE TABLE city_links"

        try:
            cursor.execute(sql_truc)
            db.commit()
        except:
            print "Error truncating city links table"
            db.rollback()

        sql_state = "SELECT id, city_name, city_url FROM city ORDER BY id ASC"
        
    	try:
    		cursor.execute(sql_state)
    		result = cursor.fetchall()

    		for row in result:
    			city_url = row[2]

    			try:
    				yield scrapy.Request(url=city_url, callback=self.parse)
    			except:
    				print "Error fetching url"

    	except Exception as e:
    		print "Error getting sate urls ", e

    def parse(self, response):
        cu_id = 0
        
        sql_county = "SELECT id FROM city WHERE city_url = '%s' " % (response.url)
        
    	try:
    		cursor.execute(sql_county)
    		row = cursor.fetchone()
    		cu_id = row[0]
    	except Exception as e:
    		print "Error fetching city with url ", e
    		
        for tag in response.css('div.panel-body ul.content_directory li'):
        	link_title = str(tag.css('h4 a::text').extract_first().strip())
        	link_url = str(tag.css('h4 a::attr(href)').extract_first().strip())
        	link_desc = str(tag.css('span::text').extract_first().strip())
        	
        	sql_ins = "INSERT INTO city_links(city_id, link_title, link_url, link_desc, final_url_reached) \
        				VALUES('%s', '%s', '%s', '%s', '%s') " % (cu_id, link_title, link_url, link_desc, '1')
        	
        	try:
        		cursor.execute(sql_ins)
        		db.commit()
        	except Exception as e:
        		db.rollback()
        		print "Error inserting data to city links table 1", e
        		
        	yield {
        		'city_id': cu_id,
        		'link_title': link_title,
        		'link_desc': link_desc,
        		'link_url': link_url
        	}

        # for tag in response.css('div.panel-body ul.Q-A-sec li'):
        # 	link_title = str(tag.css('h4 a::text').extract_first().strip())
        # 	link_url = str(tag.css('h4 a::attr(href)').extract_first().strip())
        # 	link_desc = '' #str(tag.css('span::text').extract_first().strip())
        	
        # 	sql_ins = "INSERT INTO city_links(city_id, link_title, link_url, link_desc, final_url_reached) \
        # 				VALUES('%s', '%s', '%s', '%s', '%s') " % (cu_id, link_title, link_url, link_desc, '1')
        	
        # 	try:
        # 		cursor.execute(sql_ins)
        # 		db.commit()
        # 	except Exception as e:
        # 		db.rollback()
        # 		print "Error inserting data to city links table 2", e
        		
        # 	# yield {
        # 	# 	'city_id': cu_id,
        # 	# 	'link_title': link_title,
        # 	# 	'link_desc': link_desc,
        # 	# 	'link_url': link_url
        # 	# }
