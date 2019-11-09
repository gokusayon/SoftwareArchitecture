from flask import Flask, jsonify, Request
from flask import request
from pexpect import pxssh
import logging
import requests, boto3, botocore, paramiko

key = paramiko.RSAKey.from_private_key_file("./docker.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

app = Flask(__name__)
app.secret_key = 'key'

instance_ip = "ec2-13-233-3-116.ap-south-1.compute.amazonaws.com"
username = "ec2-user"

count=0
accepted = 0
rejected = 0
last_rejected = 0
last_accepted = 0

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

class Rules:
    def ssh(self):
    	# Connect/ssh to an instance
    	try:
    	    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    	    client.connect(hostname=instance_ip, username=username, pkey=key)
    
    	    # Execute a command(cmd) after connecting/ssh to an instance
    	    stdin, stdout, stderr = client.exec_command('ls -l')
    	    r = stdout.read()
    
    	    # close the client connection once the job is done
    	    client.close()
    	    return r
    
    	except ValueError:
    	    return "error"
        
    def http(self):
    	# Connect/ssh to an instance
    	try:
    	    r = requests.get('http://www.google.com/search?q=software+architecture');
    	    return r.text
    
    	except ValueError:
    	    return "error"
        
    def network(self):
    	return "Accessing another Network!"

rules = Rules()

@app.route('/safety_wrapper/<string:type>')
def is_valid_request(type):
	global count,accepted ,last_rejected ,last_accepted ,rejected 
	logger = get_module_logger("safety_wrapper") 

	try:
		if(count < 100):
			count+=1
			accepted+=1
			last_rejected+=1
			last_accepted=0
			method = getattr(rules, type)
			result = method()
			count-=1
			return result
		else:			
			rejected+=1
			last_accepted+=1
			last_rejected=0
			return jsonify({'count': count,'error':'Unable to serve request right now. Please come again later.'})
	except ValueError:
		return "Error Accessing Network"

	if last_rejected == 0:
		print(" ============== rejected ==============")
		logger.info(f"count : {count} , status : 'success', accepted : {accepted}, accepted : {rejected}, last_rejected : {last_rejected}, last_accepted : {last_accepted}")
		return
	print(f"count : {count} , status : 'success', accepted : {accepted}, accepted : {rejected}, last_rejected : {last_rejected}, last_accepted : {last_accepted}")
	logger.info(f"count : {count} , status : 'success', accepted : {accepted}, accepted : {rejected}, last_rejected : {last_rejected}, last_accepted : {last_accepted}")

@app.route('/')
def ping():
	return "Ping Successfull!"

@app.route('/set_count/<int:c>')
def set_count(c):
	logger = get_module_logger("set_count") 
	global count
	count = c
	logger.info(f"count : {count} , status : 'success', accepted : {accepted}, accepted : {rejected}, last_rejected : {last_rejected}, last_accepted : {last_accepted}")
	return jsonify({'count': count,'success':'Count value updated successfully.'})

	
if __name__ == '__main__':
   logging.basicConfig(filename='app.log',level=logging.INFO)
   app.run(host='0.0.0.0', port=80, debug=True)


