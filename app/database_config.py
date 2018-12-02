import psycopg2
import os


DB_HOST = 'localhosr'
DB_USERNAME = 'n'
DB_NAME = 'ireporterflask'
DB_PASS = '123456'
DB_PORT = '5432'

url = "dbname='ireporterflask host='localhost'\
              port='5432' user='n' password='123456'"

db_url = os.getenv(['DATABASE_URL'])

print(db_url)

# creating the connection
con = psycopg2.connect(url)

# creating the cursor
cur = con.cursor()

# Executing the sql query
result = con.execute()

# Closing the connection
con.close()
