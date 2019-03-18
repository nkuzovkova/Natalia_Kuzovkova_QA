import logging
import os
import random
import string
import sys
from datetime import datetime
from io import StringIO
import time


class Log:

    log_stream = StringIO()
    filename = None

    @classmethod
    def get_file(cls, level):
        if cls.filename is None:
            cls.filename = os.path.join(os.path.join(os.getcwd(), "test\\logs\\"), datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S") + '.log')
            fh = logging.StreamHandler(sys.stdout)
            fh.setLevel(level)
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            fh.setFormatter(formatter)
            logging.getLogger().addHandler(fh)
            logging.getLogger().setLevel(level)

    @classmethod
    def info(cls, message):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', stream=cls.log_stream)
        Log.get_file(logging.DEBUG)
        logging.info(message)

    @classmethod
    def error(cls, message):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', stream=cls.log_stream)
        Log.get_file(logging.DEBUG)
        logging.error(message)


class Random:

    @staticmethod
    def rand_char_string(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def rand_int_string(length):
        return ''.join(random.choice(string.digits) for _ in range(length))

    @staticmethod
    def rand_string(length):
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_obj_key(obj_cls, *args, **kwargs):
    return str(obj_cls) + str(args) + str(kwargs)