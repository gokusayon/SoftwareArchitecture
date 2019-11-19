from flask import Flask, jsonify, Request, url_for
from flask import request
import json
from pexpect import pxssh
import logging
import requests
import paramiko
from AppInterface import AppInterface

key = paramiko.RSAKey.from_private_key_file("./docker.pem")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

app = Flask(__name__)
app.secret_key = 'appkey'

instance_ip = "ec2-13-233-3-116.ap-south-1.compute.amazonaws.com"
username = "ec2-user"


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

logger = get_module_logger("safety_wrapper")

class AuthenticateRequests(AppInterface):
    def __init__(self):
        self.count = 0
        self.accepted = 0
        self.last_rejected = 0
        self.last_accepted = 0
        self.rejected = 0

    def doSSH(self):
        # Connect/ssh to an instance
        try:
            # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
            logger.info(f"hostname : {self.hostname}, username : {self.username}")
            client.connect(hostname=self.hostname, username=self.username, pkey=key)
    
            # Execute a command(cmd) after connecting/ssh to an instance
            stdin, stdout, stderr = client.exec_command('ls -l')
            r = stdout.read()
    
            # close the client connection once the job is done
            client.close()
            return r
    
        except ValueError:
            return "error"
    def network_call(self):
        # Connect/ssh to an instance
        try:
            r = requests.get(self.hostname);
            return r.text
    
        except ValueError:
            return "error"

    def initiate(self,json):        
        #logger.info(f"Request Type : {self.type}, count : {self.count} , status : success, accepted : {self.accepted}, \
        #    rejected : {self.rejected}, self.last_rejected : {self.last_rejected}, self.last_accepted : {self.last_accepted}")
        try:
            if json['type'] == 'network_call':
                self.set_networkcall_params(json['hostname'],json['port'])
            else:
                #logger.info(f"hostname : {json['hostname']}, username : {json['username']}")
                self.set_ssh_params(json['hostname'], json['username'])
            method = getattr(self, json['type'])
            result = method()
            return result
        except ValueError:
            logger.error("Unable to serve request ...")
            return "Error Accessing Network"
    

auth = AuthenticateRequests()

@app.route('/safety_wrapper', methods=['GET','POST'])
def is_valid_request():
    json = request.get_json()
    print(json)
    return auth.initiate(json)
    #return r
#    return {'status' : True}

@app.route('/ping')
def ping():
	return "Python Wrapper!!"

@app.route('/set_count/<int:c>')
def set_count(c):
	auth.count = c
	logger.info(f"count : {auth.count}, status : success, accepted : {auth.accepted}, \
            rejected : {auth.rejected}, auth.last_rejected : {auth.last_rejected}, auth.last_accepted : {auth.last_accepted}")
	return jsonify({'count': auth.count,'success':'Count value updated successfully.'})

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
# Retuns all the mapped URL's
@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return json.dumps(links)
    # links is now a list of url, endpoint tuples
if __name__ == '__main__':
   logging.basicConfig(filename='app.log',level=logging.INFO)
   app.run(host='0.0.0.0', port=80, debug=True)


