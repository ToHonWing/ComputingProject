from flask import Flask, request, jsonify
from time import time
import redis
from logger import loggerConfig
from configLoader import configLoader

class RateLimiter:

    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    config = configLoader()
    loadLogger = loggerConfig()
    requestLogger = loadLogger.configure_logging('WAFX')
    # Rate limit configuration
    get_request = config.read_config('RATE_LIMIT','request')  # number of requests
    get_time = config.read_config('RATE_LIMIT','time')  # time window in seconds
    RATE_LIMIT = int(get_request)
    TIME_WINDOW = int(get_time)

    def rate_limit(self, ip):
        current_time = time()
        key = f"rate_limit:{ip}"
        
        # Fetch request timestamps
        request_times = self.redis_client.lrange(key, 0, -1)
        request_times = [float(ts) for ts in request_times]

        # Filter out requests that are outside of the time window
        request_times = [timestamp for timestamp in request_times if current_time - timestamp < self.TIME_WINDOW]

        if len(request_times) >= self.RATE_LIMIT:
            return False
        else:
            # Add the current timestamp to the list
            self.redis_client.lpush(key, current_time)
            # Trim the list to the most recent RATE_LIMIT timestamps
            self.redis_client.ltrim(key, 0, self.RATE_LIMIT - 1)
            # Set the expiration of the key
            self.redis_client.expire(key, self.TIME_WINDOW)
            return True

    def before_request(self):
        client_ip = request.remote_addr
        if not self.rate_limit(client_ip):
            return jsonify({"error": "rate limit exceeded"}), 429