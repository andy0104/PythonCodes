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

class CulinkSpider(scrapy.Spider):
    name = "culink"
    #allowed_domains = ["example.com"]
    #start_urls = ['http://example.com/']
    
    def start_requests(self):
    	sql_truc = "TRUNCATE TABLE county_links"

        try:
            cursor.execute(sql_truc)
            db.commit()
        except:
            print "Error truncating county links table"
            db.rollback()

        sql_state = "SELECT id, county_name, county_url FROM county ORDER BY id ASC"
        
    	try:
    		cursor.execute(sql_state)
    		result = cursor.fetchall()

    		for row in result:
    			county_url = row[2]

    			try:
    				yield scrapy.Request(url=county_url, callback=self.parse)
    			except:
    				print "Error fetching url"

    	except Exception as e:
    		print "Error getting sate urls ", e

    def parse(self, response):
        cu_id = 0
        
        sql_county = "SELECT id FROM county WHERE county_url = '%s' " % (response.url)
        
    	try:
    		cursor.execute(sql_county)
    		row = cursor.fetchone()
    		cu_id = row[0]
    	except Exception as e:
    		print "Error fetching county with url ", e
    		
        for tag in response.css('div.panel-body ul.content_directory li'):
        	link_title = str(tag.css('h4 a::text').extract_first().strip())
        	link_url = str(tag.css('h4 a::attr(href)').extract_first().strip())
        	link_desc = str(tag.css('span::text').extract_first().strip())
        	
        	sql_ins = "INSERT INTO county_links(county_id, link_title, link_url, link_desc, final_url_reached) \
        				VALUES('%s', '%s', '%s', '%s', '%s') " % (cu_id, link_title, link_url, link_desc, '1')
        	
        	try:
        		cursor.execute(sql_ins)
        		db.commit()
        	except Exception as e:
        		db.rollback()
        		print "Error inserting data to county links table ", e
        		
        	yield {
        		'county_id': cu_id,
        		'link_title': link_title,
        		'link_desc': link_desc,
        		'link_url': link_url
        	}

