from flask import Flask, request, Response, abort
from logger import loggerConfig
from configLoader import configLoader

class cmInjection:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    
    CM_INVALID = config.read_config('CMINJECTION','invalid').split(',')
    def block_cm_injection(self):
        # Check for common SQL injection patterns in query parameters
        for value in request.values.values():
            print(f'1: {value}')
            for sql_value in self.CM_INVALID:
                print(f'2: {sql_value}')
                if sql_value in value:
                    self.requestLogger.info(f'Command injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) 