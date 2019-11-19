from flask import Flask, jsonify
import json, requests
import threading
import logging
from AppInterface import AppInterface

app = Flask(__name__)
app.secret_key = 'key'

class Req(AppInterface):
	def get_ssh_params(self):
		return self.hostname, self.username, self.pkey
	def get_networkcall_params(self):
		return self.hostname, self.port, self.param, self.body
	def serialize(self):
		if type == 'ssh':
			return {'hostname': self.hostname,'username': self.username,'pkey': self.pkey}
		else:
			return {'hostname': self.hostname,'port': self.port,'param': self.param, 'body': self.body}

def get_module_logger(name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
 
logger = get_module_logger("python_app")
  
def init_ssh_connection():
	""" 
	function to print cube of given num 
	"""
	try:
		req = Req('doSSH')
		req.set_networkcall_params('http://www.google.com/search?q=software+architecture', 80)
		print(req.serialize())
		# r = requests.get('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper/ssh')
		logger.info(f"Req: {req.serialize()}")

	except ValueError:
		logger.info(f"error -- ssh")
  
def init_network_request():
	""" 
	function to print square of given num 
	"""
	try:
		r = requests.get('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper/network')
		logger.info(f"Status Code : {r.status_code}")

	except ValueError:
		logger.info(f"error -- network")
  
def init_http_request():
	"""
	function to print square of given num
	"""
	try:
		r = requests.get('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper/http')
		logger.info(f"Status Code : {r.status_code}")
	except ValueError:
		logger.info(f"error -- http")

def start_threads(): 
    # creating thread 
    logger.info(f"Starting Threads")
    t1 = threading.Thread(target=init_ssh_connection, name='t1') 
    t2 = threading.Thread(target=init_network_request, name='t2')  
    t3 = threading.Thread(target=init_http_request, name='t3')   
  
    # starting threads 
    t1.start() 
    t2.start() 
    t3.start() 
    
    # both threads completely executed 
    logger.info(f"Done!")

@app.route('/initiate')
def initiate():
	init_ssh_connection()
	return {'status' : 'success'}


@app.route('/ping')
def ping():
	return jsonify({'status':'success', 'message': "Python Main App!!"})

	
if __name__ == '__main__':
   logging.basicConfig(filename='app.log',level=logging.INFO)
   app.run(host='0.0.0.0', port=8080)