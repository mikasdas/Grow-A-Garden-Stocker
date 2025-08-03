import logging
import sys
import os

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[37m",    # white
        logging.INFO: "\033[36m",     # cyan
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",    # red
        logging.CRITICAL: "\033[41m", # red
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

"""
logging.basicConfig(level=logging.INFO,
                    filename='data/logs/log.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S'
                    )
"""

def create_logger(name, file_path, consol):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)


    if not logger.hasHandlers():
        # File Handler
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        
        if consol is True:
            logger.addHandler(console_handler)

        return logger

logs_logger = create_logger('Info_logger', 'data/logs/logs.log', True)
stock_logger = create_logger('Stock_logger', 'data/logs/Stock.log', False)
important_logger = create_logger('Important_logger', 'data/logs/Stock.log', True)