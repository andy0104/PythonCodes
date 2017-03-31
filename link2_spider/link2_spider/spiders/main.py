# -*- coding: utf-8 -*-
import scrapy
import MySQLdb

try:
    # Open database connection
    #db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
    db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler_2', unix_socket = '/opt/lampp/var/mysql/mysql.sock')
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
    #allowed_domains = ["example.com"]
    #start_urls = ['http://example.com/']

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

    	urls = ['https://brbpublications.com/freesites/freesites.aspx']
    	for url in urls:
    		yield scrapy.Request(url=url, callback=self.parse_state)

    def parse_state(self, response):
        


