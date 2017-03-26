import scrapy
import MySQLdb
import urllib2

# Open database connection
#db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
try:
    db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'web_crawler', unix_socket = '/opt/lampp/var/mysql/mysql.sock')
    print "Db connected"
except Exception as e:
    print "Cannot connect to db"
    print e

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM city_links WHERE is_update_url = '%s' " % ('0')

try:
    # Execute the SQL command
    cursor.execute(sql)

    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        county_id = row[1]
        link_url = row[3]

        tmp_url = link_url
        print tmp_url

        try:
            link_url = urllib2.urlopen(link_url, None, 1).geturl()#get_final_url(link_url)
        except Exception as e:
            print "Final url error: ", e

        if tmp_url != link_url:
            final_url_reached = '1'
        else:
            final_url_reached = '0'

        sql_update = "UPDATE city_links SET link_url = '%s', final_url_reached = '%s', is_update_url = '%s' WHERE \
                    id = '%s' " % (link_url, final_url_reached, '1', id)

        try:
            cursor.execute(sql_update)
            # Commit your changes in the database
            db.commit()
        except Exception as e:
            # Rollback in case there is any error
            db.rollback()
            print "Update SQL Failed ", e

except Exception as e:
    print "Unable to fetch data"
    print e
finally:
    # disconnect from server
    db.close()

def get_final_url(link_url):
    try:
        link_url = urllib2.urlopen(link_url, None, 1).geturl()
    except:
        print "N F: " + link_url
        print "Could not get final url"

    return link_url
