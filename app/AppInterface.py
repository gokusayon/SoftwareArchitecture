# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 23:53:14 2019

@author: vasum
"""
from abc import abstractmethod
class AppInterface:
    def __init__(self, type):
        self.type = type
    def set_ssh_params(self, hostname, username, pkey):
        self.hostname = hostname
        self.username = username
        self.pkey = pkey
    def set_networkcall_params(self, hostname, port , param = None, body = None):
        self.hostname = hostname
        self.port = port
        self.param = param
        self.body = body
    def get_ssh_params(self):
        return self.hostname, self.username, self.pkey
    
    def get_networkcall_params(self):
        return self.hostname, self.port, self.param, self.body    
    def doSSH(self):
        pass

#    @abstractmethod
    @abstractmethod
    def network_call(self):
        pass
    @abstractmethod
    def initialize(self):
        pass
    def serialize(self):
        if type == 'ssh':
            return {'hostname': self.hostname,'username': self.username,'pkey': self.pkey}
        else:
            return {'hostname': self.hostname,'port': self.port,'param': self.param, 'body': self.body }