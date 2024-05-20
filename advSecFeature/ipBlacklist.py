from flask import Flask, request, Response, abort
from urllib.parse import urlparse
from proxyHandler  import proxyHandler
from logger import loggerConfig
from configLoader import configLoader

class ipBlacklist:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    ip_blacklist = config.read_config('IP_BLACKLIST','ip').split(',')
    
    def block_ip(self):
        client_ip = request.remote_addr
        if client_ip in self.ip_blacklist:
            self.requestLogger.info(f'IP blocked from: {request.remote_addr} to {request.base_url}')
            abort(403) 