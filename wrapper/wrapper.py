from flask import Flask, jsonify
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

@app.route('/ssh')
def request():
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

@app.route('/')
def ping():
	return "Hello World!"

	
if __name__ == '__main__':
   logging.basicConfig(filename='app.log',level=logging.DEBUG)
   app.run(host='0.0.0.0', port=80, debug=True)


