from AppInterface import AppInterface
import json, requests

from AppInterface import AppInterface

class Req(AppInterface):
  @property
  def serialize(self):
    if self.type == 'doSSH':
      return {'type': self.type, 'hostname': self.hostname,'username': self.username}
    else:
      return {'type': self.type, 'hostname': self.hostname,'port': self.port,'param': self.param, 'body': self.body}

def init_network_request():
    """ 
    function to print square of given num 
    """
    try:
        req = Req('network_call')
        req.set_networkcall_params('https://duckduckgo.com/?&t=hg', 8080)
        data = {
          "type" : "network_call",
          "hostname" : "https://duckduckgo.com/?&t=hg",
          "port" : 80
        }
        r = requests.post('http://ec2-52-66-158-41.ap-south-1.compute.amazonaws.com/safety_wrapper', json = req.serialize)
        return r.status_code

    except ValueError:
        logger.info(f"error -- network")

print(init_network_request())