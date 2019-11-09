from flask import Flask, jsonify
import json


from flask import url_for, redirect

app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/ssh', methods=['GET', 'POST'])
def ssh():
	
	return "Hello"


@app.route('/ping')
def ping():
	return "Hello World!"

	
if __name__ == '__main__':
   import logging
   logging.basicConfig(filename='app.log',level=logging.DEBUG)
   app.run(host='0.0.0.0', port=8080)