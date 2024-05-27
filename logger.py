import logging
from logging.handlers import RotatingFileHandler

class loggerConfig:
    
    def configure_logging(self, name):

            # Create a logger object
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)  # Set the minimum level to handle

            # Create handlers for logging (console and file handler)
            console_handler = logging.StreamHandler()
            file_handler = RotatingFileHandler('/opt/WAFX/log/waf.log', maxBytes=10000, backupCount=3)
            
            # Set the level of logging for each handler
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # Add handlers to the logger
            if (logger.hasHandlers()):
                logger.handlers.clear()
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

            return logger