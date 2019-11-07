from flask import Flask, render_template, request, flash, jsonify
import json
import pymysql


from flask import url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug import secure_filename

app = Flask(__name__,template_folder='templates',static_folder='/home/ec2-user/downloads/')
app.secret_key = 'development key'

databaseServerIP = "database-3.csso1whzul3i.ap-south-1.rds.amazonaws.com"  # IP address of the MySQL database server
databaseUserName = "admin"       # User name of the database server
databaseUserPassword = "12341234"    # Password for the database user

newDatabaseName = "DB_PHOTO_GALLARY_V6" # Name of the database that is to be created
charSet = "utf8mb4"     # Character set
cusrorType = pymysql.cursors.DictCursor

table_name = "TB_IMAGE_V1"

@app.route('/create_db', methods = ['GET', 'POST'])
def create_db():
	
	# Create New Database
	
	global databaseServerIP
	global databaseUserName
	global databaseUserPassword
	global newDatabaseName
	global charSet
	global cusrorType
	global table_name
	
	connectionInstance = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,charset=charSet,cursorclass=cusrorType)
	   
	try:
		cursorInsatnce = connectionInstance.cursor()
		sqlStatement = "CREATE DATABASE "+ newDatabaseName
		cursorInsatnce.execute(sqlStatement)
		
		# sqlQuery = "SHOW DATABASES"
		# cursorInsatnce.execute(sqlQuery)
		# databaseList = cursorInsatnce.fetchall()

		# for datatbase in databaseList:
			# print(datatbase)
	
	except Exception as e:
		print("Exeception occured:{}".format(e))
	finally:
		connectionInstance.close()
	
	connectionObject   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,db=newDatabaseName, charset=charSet,cursorclass=cusrorType)
	
	# Create New Table
	try:
		cursorObject        = connectionObject.cursor()
		sqlCreateTableCommand   = "CREATE TABLE "+ table_name +" (id int(11) AUTO_INCREMENT PRIMARY KEY,name varchar(100), img LONGBLOB)"
		cursorObject.execute(sqlCreateTableCommand)
		
		
		# sqlQuery            = "show tables"   
		# cursorObject.execute(sqlQuery)
		# rows                = cursorObject.fetchall()
		# for row in rows:
			# print(row)

	except Exception as e:
		print("Exeception occured:{}".format(e))

	finally:
		connectionObject.close()
	
	return "db created"


@app.route('/check', methods = ['GET', 'POST'])
def check():

	global databaseServerIP
	global databaseUserName
	global databaseUserPassword
	global newDatabaseName
	global charSet
	global cusrorType
	global table_name

	connectionObject1   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,db=newDatabaseName, charset=charSet,cursorclass=cusrorType)
		
	try:
		cursorObject        = connectionObject1.cursor()
		sqlQuery            = "DESCRIBE "+table_name
		cursorObject.execute(sqlQuery)
		
		temp                = cursorObject.fetchall()
		
		print(temp)
		

	except Exception as e:
		print("Exeception occured:{}".format(e))

	finally:
		connectionObject1.close()
		
	return "upload page"
 
class UploadForm(FlaskForm):
	file = FileField()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	return render_template('upload.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
	form = UploadForm()
	return "Hello"




@app.route('/uf', methods=['GET', 'POST'])
def upload_file():
	file = request.files['inputFile']
	
	count = 0
	
	# print(file.filename)
		
	global databaseServerIP
	global databaseUserName
	global databaseUserPassword
	global newDatabaseName
	# global charSet
	# global cusrorType
	global table_name
	
	connectionObject   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,db=newDatabaseName)

	try:
		# Create a cursor object
		cursorObject = connectionObject.cursor()                                     

		sql="SELECT id FROM TB_IMAGE_V1 ORDER BY id DESC LIMIT 1"
		cursorObject.execute(sql)
		last_id = cursorObject.fetchone()
   
		print(last_id)
		#count = count + last_id + 1

		new_file = file.read()

		# Insert rows into the MySQL Table
		insertStatement = "INSERT INTO " + table_name + "(id,name,img) VALUES(%s,%s,%s)"   
		
		blob_tuple = (count,file.filename,new_file)
		
		cursorObject.execute(insertStatement,blob_tuple)
		# count = count + 1
		
		# Get the primary key value of the last inserted row
		# print("Primary key id of the last inserted row:")
		

	except Exception as e:
		print("Exeception occured:{}".format(e))

	finally:
		connectionObject.commit()
		
	# return "same page"
	return redirect("http://ccloadbalancer-47627977.ap-south-1.elb.amazonaws.com")

def config():
	global databaseServerIP
	global databaseUserName
	global databaseUserPassword
	global newDatabaseName
	# global charSet
	# global cusrorType
	global table_name
	
	connectionObject   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,db=newDatabaseName)
	cursorObject = connectionObject.cursor() 
	return cursorObject


@app.route('/search', methods=['GET', 'POST'])
def search():
	return render_template("search.html")

@app.route('/show', methods=['GET', 'POST'])
def show():
		
	global databaseServerIP
	global databaseUserName
	global databaseUserPassword
	global newDatabaseName
	# global charSet
	# global cusrorType
	global table_name
	
	connectionObject   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,db=newDatabaseName)
	iname = ""
	try:
		# Create a cursor object
		cursorObject = connectionObject.cursor()    
		name = request.form['filename']                                 

		sqlQuery    = "select * from "+table_name    + " where id=" + name
		print(sqlQuery)

		#Fetch all the rows - for the SQL Query
		cursorObject.execute(sqlQuery)
		row = cursorObject.fetchone()

		# for row in rows:
		image = row[2]
		photo = "/home/ec2-user/downloads/"+row[1]

		iname = row[1]
		
		
		write_file(image,photo)

	except Exception as e:
		print("Exeception occured:{}".format(e))

	finally:
		connectionObject.commit()
	print(iname)
	return render_template("show_image.html", fname = iname)


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

import json

@app.route('/all')
def all():
	cursor = config()
	global table_name
	query = "select * from " + table_name
	data = cursor.execute(query)
	rows = cursor.fetchall()

	rows = [{'id' : row[0], 'name' : row[1]} for row in rows]
	jsonData = jsonify(rows)

	return jsonData


@app.route('/ping')
def ping():
	return "Hello World!"

	
if __name__ == '__main__':
   import logging
   logging.basicConfig(filename='app.log',level=logging.DEBUG)
   app.run(host='0.0.0.0', port=8080)