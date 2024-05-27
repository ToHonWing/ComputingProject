from flask import request, abort
from urllib.parse import urlparse
from logger import loggerConfig
from configLoader import configLoader

class urlWhitelist:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    URL_WHITELIST = config.read_config('URL_WHITELIST','url').split(',')
    
    def is_valid_url(self, url):
        
        parsed_url = urlparse(url)
        # Check if the domain is in the whitelist
        if any(parsed_url.netloc == urlparse(whitelisted_url).netloc for whitelisted_url in self.URL_WHITELIST):
            return True
        return False

    def ssrf_prevention(self):
        # Check all URLs in the query parameters to prevent SSRF
        for value in request.values.values():
            if 'https' in value:   
                if not self.is_valid_url(value):
                    self.requestLogger.info(f'SSRF detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403)  
            if 'http' in value:   
                if not self.is_valid_url(value):
                    self.requestLogger.info(f'SSRF detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403) # Block the request if the URL is not valid