import MySQLdb

# Open database connection
#db = MySQLdb.connect("localhost", "root", "", "shop_trade_online", unix_socket = '/opt/lampp/var/mysql/mysql.sock')
db = MySQLdb.connect( host = 'localhost', user = 'root', passwd = '', db = 'shop_trade_online', unix_socket = '/opt/lampp/var/mysql/mysql.sock')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM intro2"

try:
    # Execute the SQL command
   cursor.execute(sql)

   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      id = row[0]
      email = row[1]
      mobile = row[2]

      # Now print fetched result
      print "id=%s, email=%s, mobile=%s " % \
             (id, email, mobile)

except:
    print "Unable to fetch data"

# disconnect from server
db.close()
