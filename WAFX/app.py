from flask import Flask, request, Response, abort
from urllib.parse import urlparse
from proxyHandler  import proxyHandler
from logger import loggerConfig
from configLoader import configLoader
from AttackDetection.sqlInjection import sqlInjection
from AttackDetection.xssDectection import xssDetection
from AttackDetection.cmInjection import cmInjection
import re

app = Flask(__name__)
proxyObj = proxyHandler()
logger = loggerConfig()
config = configLoader()
sqlInject = sqlInjection()
xssDetect = xssDetection()
cmDetect = cmInjection()
wafLogger = logger.configure_logging('WAFX')

# The URL of the web server to which the WAF should forward the requests
#WEB_SERVER_URL = config.read_config('SERVER','url1')
URL_WHITELIST = config.read_config('URL_WHITELIST','url').split(',')
#SQL_INVALID = config.read_config('SQL','invalid').split(',')

# Define your security checks
@app.before_request
def blockSqlInject():
    return sqlInject.block_sql_injection()

@app.before_request
def blockXSS():
    return xssDetect.block_XSS()

@app.before_request
def blockCMInject():
    return cmDetect.block_cm_injection()
'''
def block_sql_injection():
    # Check for common SQL injection patterns in query parameters
    for value in request.values.values():
        for sql_value in SQL_INVALID:
            if sql_value.upper() in value.upper():
                wafLogger.info(f'injection detected from: {request.remote_addr} to {request.base_url} input: {value}')
                abort(403) 
                '''
    #return request

#@app.before_request
#def check_request():
    # Run your security checks
    #if block_sql_injection():
        #abort(403) 

# Proxy logic to forward requests to the web server and get the response
            
            
PRIVATE_IP_REGEX = re.compile(
    r'localhost|127(?:\.[0-9]+){0,2}\.[0-9]+|'
    r'(?:10|172(?:\.1[6-9]|\.2[0-9]|\.3[0-1])|192\.168)(?:\.[0-9]+){2}'
)

def is_valid_url(url):
    parsed_url = urlparse(url)
    # Check if the domain is in the whitelist
    if any(parsed_url.netloc == urlparse(whitelisted_url).netloc for whitelisted_url in URL_WHITELIST):
        return True
    # Check if it is a private IP address
    #if PRIVATE_IP_REGEX.match(parsed_url.hostname):
        #return False
    # Add more checks if necessary (like checking for localhost, etc.)
    # ...
    return False

@app.before_request
def ssrf_prevention():
    # Check all URLs in the query parameters to prevent SSRF
    for value in request.values.values():
        if 'http' in value:   
            if not is_valid_url(value):
                logger.info("SSRF detected: " + value)
                abort(403)  # Block the request if the URL is not valid

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxyhandler(path):
    return proxyObj.proxy(path)

wafLogger.info("WAFX is active")
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5002)
    app.run()
    