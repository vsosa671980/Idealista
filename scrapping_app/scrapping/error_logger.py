import os
import sys
# get current directory
path = os.path.dirname(__file__)
# parent directory
parent = os.path.dirname(path)
grandParent = os.path.dirname(parent)
# appending a path
sys.path.append(grandParent)
import logging
from scrapping_app.scrapping.config import ERROR_LOG_FILE_NAME

def log_error(error_message):
    try:
        logging.basicConfig(filename=ERROR_LOG_FILE_NAME,
                            level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(error_message, exc_info=True)
    except Exception as e:
        print("Error during error logging")
        print(e)

def print_log_error():
    try:
        logging.basicConfig(filename=ERROR_LOG_FILE_NAME, level=logging.ERROR)
        with open(ERROR_LOG_FILE_NAME, 'r') as f:
            errors = f.readlines()
        for error in errors:
            print(error)
    except Exception as e:
        print("Error during error log printing")
        print(e)

