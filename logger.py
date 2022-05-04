import logging,logging.handlers
import datetime

class log_module():

    def __init__(self):

        # set up self.logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        datefmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s: %(message)s')
        logFilename = 'log_files/dicom_deidentify_program.log'
        handler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=1000000, backupCount=10)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info('Logger module has been Initialized')


