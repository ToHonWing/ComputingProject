from flask import Flask, request, Response, abort
from urllib.parse import urlparse
from proxyHandler  import proxyHandler
from logger import loggerConfig
from configLoader import configLoader

class httpMethodRestrict:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    allow_method = config.read_config('HTTP_METHOD','method').split(',')
    
    def method_filter(self):
        if request.method not in self.allow_method:
            self.requestLogger.info(f'HTTP {request.method} block from: {request.remote_addr} to {request.base_url}')
            abort(405)  # Method Not Allowed