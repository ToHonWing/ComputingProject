from flask import Flask, request, Response, abort
from logger import loggerConfig
from configLoader import configLoader

class sqlInjection:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    
    SQL_INVALID = config.read_config('SQL','invalid').split(',')
    def block_sql_injection(self):
        # Check for common SQL injection patterns in query parameters
        for value in request.values.values():
            for sql_value in self.SQL_INVALID:
                if sql_value.upper() in value.upper():
                    self.requestLogger.info(f'SQL injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) 