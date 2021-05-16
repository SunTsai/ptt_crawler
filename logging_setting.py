import os
import logging

format = '%(asctime)s [%(filename)s: %(lineno)d] %(levelname)s %(process)d: %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(format, datefmt)
        
class Log:
    def __init__(self, log_dir):
        self.log_dir = log_dir

    def create_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        file_handler = logging.FileHandler(os.path.join(self.log_dir, logger_name))
        file_handler.setFormatter(formatter)

        logger.addHandler(console)
        logger.addHandler(file_handler)


