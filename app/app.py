from flask import Flask, jsonify
import json, requests, time
import threading
import logging
from AppInterface import AppInterface
import multiprocessing

app = Flask(__name__)
app.secret_key = 'key'
timer =0.1
class Req(AppInterface):
  @property
  def serialize(self):
    if self.type == 'doSSH':
      return {'type': self.type, 'hostname': self.hostname,'username': self.username}
    else:
      return {'type': self.type, 'hostname': self.hostname,'port': self.port,'param': self.param, 'body': self.body}

def get_module_logger(name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
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
	    req.set_ssh_params("ec2-13-233-3-116.ap-south-1.compute.amazonaws.com", "ec2-user")
	    logger.info(f"Req: {req.serialize}")
	    r = requests.post('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper', json = req.serialize)
	    return r.text, r.status_code
  
	except ValueError:
		logger.info(f"error -- ssh")

def init_network_request():
    """ 
    function to print square of given num 
    """
    try:
        req = Req('network_call')
        req.set_networkcall_params('https://duckduckgo.com/?&t=hg', 8080)
        logger.info(f"Req : {req.serialize}")
        r = requests.post('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper', json = req.serialize)
        return r.text, r.status_code

    except ValueError:
        logger.info(f"error -- network")

def start_threads(): 
    # creating thread 
    logger.info(f"Starting Threads")
    t1 = threading.Thread(target=init_ssh_connection, name='t1') 
    t2 = threading.Thread(target=init_network_request, name='t2') 
  
    # starting threads 
    t1.start() 
    t2.start() 
    
    # both threads completely executed 
    logger.info(f"Done!")

def init_req():
    ssh, ssh__status_code = init_ssh_connection()
    nc, nc_status_code = init_network_request()
    data = {
    "ssh" : ssh__status_code,
    "network_call" : ssh__status_code
    }
    return data


@app.route('/initiate')
def initiate():
    return init_req()

@app.route('/execute_periodically')
def execute_periodically():
    global timer
    jobs = []
    for i in range(0, 10):
        out_list = list()
        process = multiprocessing.Process(target=initiate)
        jobs.append(process)
    # Start the processes (i.e. calculate the random number lists)      
    for j in jobs:
        time.sleep(timer)
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("List processing complete.")
    return jsonify({"timer" : timer})

@app.route('/set_timer/<float:c>')
def set_count(c):
    global timer
    timer = c
    return jsonify({'timer': timer,'success':'timer value updated successfully.'})

@app.route('/ping')
def ping():
	return jsonify({'status':'success', 'message': "Python Main App!!"})

	
if __name__ == '__main__':
   logging.basicConfig(filename='app.log',level=logging.INFO)
   app.run(host='0.0.0.0', port=8080, debug=True)