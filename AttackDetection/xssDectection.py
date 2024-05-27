from flask import request, abort
from logger import loggerConfig
from configLoader import configLoader
import re

class xssDetection:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    
    SCRIPT_INVALID = config.read_config('XSS','invalid')
    
    def block_XSS(self):
        # Check for common SQL injection patterns in query parameters
        xss_pattern = re.compile(self.SCRIPT_INVALID, re.IGNORECASE | re.VERBOSE)
        for value in request.values.values():
            if xss_pattern.search(value):
                self.requestLogger.info(f'XSS detected from: {request.remote_addr} to {request.base_url} input: {value}')
                abort(403) 
            '''for xss_value in self.SCRIPT_INVALID:
                if xss_value in value:
                    self.requestLogger.info(f'XSS detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) '''