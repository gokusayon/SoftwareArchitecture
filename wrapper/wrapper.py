from flask import Flask, jsonify
import json

app = Flask(__name__)
app.secret_key = 'key'

@app.route('/')
def filter():	
	return "Filter Request"


@app.route('/ping')
def ping():
	return "Hello World!"

	
if __name__ == '__main__':
   import logging
   logging.basicConfig(filename='app.log',level=logging.DEBUG)
   app.run(host='0.0.0.0', port=80)