from flask import request, Response
import requests
from configLoader import configLoader
from logger import loggerConfig

class proxyHandler:
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    # The URL of the web server to which the WAF should forward the requests
    WEB_SERVER_URL = config.read_config('SERVER','url1')
    def proxy(self, path):
    
        # Construct the full URL to forward the request to
        dest_url = f'{self.WEB_SERVER_URL}/{path}'
        
        headers = {key: value for key, value in request.headers if key != 'Host'}
        
        response = requests.request(
            method=request.method,
            url=dest_url,
            headers=headers,
            params=request.query_string,
            cookies=request.cookies,
            allow_redirects=False,
            stream=True
        )
        
        self.requestLogger.info(f'Http method: {request.method}, url: {dest_url} from: {request.remote_addr}')
        # Create a response object, streaming the content from the backend server response
        response_content = response.raw.read(decode_content=True)
        
        custom_response = Response(response_content, response.status_code)
        
        return custom_response