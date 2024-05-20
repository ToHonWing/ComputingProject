from flask import Flask, request, Response, abort
from logger import loggerConfig
from configLoader import configLoader

class xssDetection:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    
    SCRIPT_INVALID = config.read_config('XSS','invalid').split(',')
    def block_XSS(self):
        # Check for common SQL injection patterns in query parameters
        for value in request.values.values():
            for xss_value in self.SCRIPT_INVALID:
                if xss_value in value:
                    self.requestLogger.info(f'XSS detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) 