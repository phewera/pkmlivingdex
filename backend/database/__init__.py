import logging

# setup logger
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = logging.INFO
LOG_FILE = './var/log/database.log'

logger = logging.getLogger('database')
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT)
filehandler = logging.FileHandler(LOG_FILE)
filehandler.setLevel(LOG_LEVEL)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
