from flask import Flask, jsonify
import json, requests
import threading
import logging

app = Flask(__name__)
app.secret_key = 'key'

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
 
logger = get_module_logger("client")
  
def init_ssh_connection():
	logger = get_module_logger("ssh") 
	""" 
	function to print cube of given num 
	"""
	try:
		r = requests.get('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper/ssh')
		logger.info(f"Status Code : {r.status_code}")

	except ValueError:
		logger.info(f"error -- ssh")
  
def init_network_request(): 
	logger = get_module_logger("network") 
	""" 
	function to print square of given num 
	"""
	try:
		r = requests.get('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper/network')
		logger.info(f"Status Code : {r.status_code}")

	except ValueError:
		logger.info(f"error -- network")
  
def init_http_request():
	logger = get_module_logger("http") 
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
    t1 = threading.Thread(target=init_ssh_connection, name='t1') 
    t2 = threading.Thread(target=init_network_request, name='t2')  
    t3 = threading.Thread(target=init_http_request, name='t3')   
  
    # starting threads 
    t1.start() 
    t2.start() 
    t3.start() 
  
    # wait until all threads finish 
    t1.join() 
    t2.join() 
    t3.join() 
    # both threads completely executed 
    logger.info(f"Done!")

@app.route('/initiate')
def initiate():
	# Connect/ssh to an instance
	start_threads()
	


@app.route('/ping')
def ping():
	return "Python Main App!!"

	
if __name__ == '__main__':
   logging.basicConfig(filename='app.log',level=logging.INFO)
   app.run(host='0.0.0.0', port=8080, debug=True)