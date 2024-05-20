from flask import Flask, request, Response, abort
from urllib.parse import urlparse
from proxyHandler  import proxyHandler
from logger import loggerConfig
from configLoader import configLoader
from AttackDetection.sqlInjection import sqlInjection
from AttackDetection.xssDectection import xssDetection
from AttackDetection.cmInjection import cmInjection
from advSecFeature.urlWhitelist import urlWhitelist
from advSecFeature.ipBlacklist import ipBlacklist
from advSecFeature.httpMethodRestrict import httpMethodRestrict
from RateLimiting.Ratelimiter import RateLimiter
import re

app = Flask(__name__)
proxyObj = proxyHandler()
logger = loggerConfig()
config = configLoader()
sqlInject = sqlInjection()
xssDetect = xssDetection()
cmDetect = cmInjection()
urlFilter = urlWhitelist()
wafLogger = logger.configure_logging('WAFX')
ipblocker = ipBlacklist()
httpMethod = httpMethodRestrict()
rateLimit = RateLimiter()

@app.before_request
def checkRate():
   return rateLimit.before_request()

@app.before_request
def blockSqlInject():
    return sqlInject.block_sql_injection()

@app.before_request
def blockXSS():
    return xssDetect.block_XSS()

@app.before_request
def blockCMInject():
    return cmDetect.block_cm_injection()

@app.before_request
def blockUrl():
    return urlFilter.ssrf_prevention()

@app.before_request
def blockIp():
    return ipblocker.block_ip()

@app.before_request
def blockMethod():
    return httpMethod.method_filter()

# Proxy logic to forward requests to the web server and get the response
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxyhandler(path):
    return proxyObj.proxy(path)

wafLogger.info("WAFX is active")
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5002)
    app.run()
    