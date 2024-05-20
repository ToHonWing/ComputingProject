from flask import Flask, request, Response, abort
from urllib.parse import urlparse
from proxyHandler  import proxyHandler
from logger import loggerConfig
from configLoader import configLoader
class urlWhitelist:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    URL_WHITELIST = config.read_config('URL_WHITELIST','url').split(',')
    
    def is_valid_url(self, url):
        print(f'0: {url}')
        parsed_url = urlparse(url)
        print(f'99: {parsed_url}')
        # Check if the domain is in the whitelist
        if any(parsed_url.netloc == urlparse(whitelisted_url).netloc for whitelisted_url in self.URL_WHITELIST):
            return True
        # Check if it is a private IP address
        #if PRIVATE_IP_REGEX.match(parsed_url.hostname):
            #return False
        # Add more checks if necessary (like checking for localhost, etc.)
        # ...
        return False

    def ssrf_prevention(self):
        # Check all URLs in the query parameters to prevent SSRF
        for value in request.values.values():
            print(f'1: {value},2: {request.values.values()}')
            if 'https' in value:   
                if not self.is_valid_url(value):
                    self.requestLogger.info(f'SSRF detected from: {request.remote_addr} to {request.base_url} input: {value}')
                    abort(403)  # Block the request if the URL is not valid