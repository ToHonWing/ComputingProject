from flask import request, abort
from logger import loggerConfig
from configLoader import configLoader
import re

class sqlInjection:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    
    SQL_INVALID = config.read_config('SQL','invalid')
    
    def block_sql_injection(self):
    # Simple regex to match common SQL injection patterns
        sql_injection_pattern = re.compile(self.SQL_INVALID, re.IGNORECASE | re.VERBOSE)
        for value in request.values.values():
            if sql_injection_pattern.search(value):
                self.requestLogger.info(f'SQL injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                abort(403) 
    
     
    '''
    def block_sql_injection(self):
        # Check for common SQL injection patterns in query parameters
        for value in request.values.values():
            for sql_value in self.SQL_INVALID:
                if sql_value.upper() in value.upper():
                    self.requestLogger.info(f'SQL injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) 
                    '''