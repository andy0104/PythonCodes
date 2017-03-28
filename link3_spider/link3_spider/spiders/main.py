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

class MainSpider(scrapy.Spider):
    name = "main"
    #allowed_domains = ["http://www.open-public-records.com/"]
    #start_urls = ['http://http://www.open-public-records.com//']

    def start_requests(self):
    	sql_truc = "TRUNCATE TABLE state"

        try:
            cursor.execute(sql_truc)
            db.commit()
        except:
            print "Error truncating state table"
            db.rollback()

        sql_truc = "TRUNCATE TABLE county"

        try:
            cursor.execute(sql_truc)
            db.commit()
        except:
            print "Error truncating county table"
            db.rollback()

        sql_truc = "TRUNCATE TABLE city"

        try:
            cursor.execute(sql_truc)
            db.commit()
        except:
            print "Error truncating city table"
            db.rollback()

    	urls = ['http://www.open-public-records.com/']
    	for url in urls:
    		yield scrapy.Request(url=url, callback=self.parse_state)

    def parse(self, response):
        pass

    def parse_state(self, response):

        state_id = 0

    	for tag in response.css('div.panel-body ul.btm_cols li'):
    		state_url = str(tag.css('a::attr(href)').extract_first().strip())
    		state_name = str(tag.css('a::text').extract_first().strip())

    		county_list = []
    		county_list = yield scrapy.Request(url=state_url, callback=self.parse_county)

    		sql_ins = "INSERT INTO state(state_name, state_url) VALUES('%s', '%s')" % (state_name, state_url)

    		try:
    			cursor.execute(sql_ins)
    			db.commit()
    			state_id = cursor.lastrowid    			
    		except Exception as e:
    			print "Sate insert error", e
    			db.rollback()
    		
    		yield {
    			'state_name': state_name,
    			'state_url': state_url,
    			'county_list': county_list
    		}

    def parse_county(self, response):
    	print "In parse county: ", response.url
    	county_list = []
    	state_url_id = 0
    	sql_search = "SELECT id FROM state WHERE state_url = '%s' " % (response.url)
    	print "Parse County SQL ", sql_search

        try:
            cursor.execute(sql_search)
            #db.commit()
            row = cursor.fetchone()
            state_url_id = row[0]
        except:
            print "Error searching county table"
            #db.rollback()

        for tag in response.css('select[name=County] option'):
        	county_name = str(tag.css('option::text').extract_first().strip())
        	county_url = tag.css('option::attr(value)').extract_first()
        	print "County Name: ", county_name, "County Url: ", county_url, "State ID: ", state_url_id 

        	if county_url != None or county_url != '':
        		county_url = str(tag.css('option::attr(value)').extract_first().strip())

        		city_list = []

        		try:
        			city_list = yield scrapy.Request(url=county_url, callback=self.parse_city)
        		except Exception as e:
        			print "County Url Request Error ", e

        		sql_ins = "INSERT INTO county(state_id, county_name, county_url) VALUES('%s', '%s', '%s')" % (state_url_id, county_name, county_url)

        		try:
        			cursor.execute(sql_ins)
        			db.commit()
        		except Exception as e:
        			db.rollback()
        			print "County insert error ", e

	        	c_in = {
	        		'state_id': state_url_id,
	        		'county_name': county_name,
	        		'county_url': county_url,
	        		'city_list': city_list
	        	}
        		county_list.append(c_in)

        yield county_list

    def parse_city(self, response):
    	print "In parse city: ", response.url
    	city_list = []
    	county_url_id = 0
    	state_url_id = 0
    	sql_search = "SELECT id, state_id FROM county WHERE county_url = '%s' " % (response.url)
    	print "Parse City SQL ", sql_search

    	try:
    		cursor.execute(sql_search)
    		row = cursor.fetchone()
    		county_url_id = row[0]
    		state_url_id = row[1]
    	except Exception as e:
    		print "Error searching county table ", e

    	for tag in response.css('div.panel-body table.Q-A-sec td.table-form-td-closestcities table tr td'):
    		city_name = str(tag.css('td a::text').extract_first().strip())
        	city_url = tag.css('td a::attr(href)').extract_first()
        	print "City Name: ", city_name, "City Url: ", city_url, "State ID: ", state_url_id, "County ID: ", county_url_id

        	if city_url != None or city_url != '':
        		city_url = str(tag.css('td a::attr(href)').extract_first().strip())

        		sql_ins = "INSERT INTO city(state_id, county_id, city_name, city_url) VALUES('%s', '%s', '%s', '%s')" % (state_url_id, county_url_id, city_name, city_url)

        		try:
        			cursor.execute(sql_ins)
        			db.commit()
        		except Exception as e:
        			db.rollback()
        			print "County insert error ", e

	        	c_in = {
	        		'state_id': state_url_id,
	        		'county_id': county_url_id,
	        		'city_name': city_name,
	        		'city_url': city_url
	        	}
        		city_list.append(c_in)

        return city_list