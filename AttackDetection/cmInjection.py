from flask import Flask, request, Response, abort
from logger import loggerConfig
from configLoader import configLoader
import re

class cmInjection:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    
    CM_INVALID = config.read_config('CMINJECTION','invalid')
    
    def block_cm_injection(self):
        # Check for common SQL injection patterns in query parameters
        cm_injection_pattern = re.compile(self.CM_INVALID, re.IGNORECASE | re.VERBOSE)
        for value in request.values.values():
            if cm_injection_pattern.search(value):
                self.requestLogger.info(f'Command injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                abort(403) 
            '''for sql_value in self.CM_INVALID:
                if sql_value in value:
                    self.requestLogger.info(f'Command injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) '''