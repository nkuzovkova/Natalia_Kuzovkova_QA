from src import env_file_content
import string
from random import *

# Default user name and password are specified in resources, but it is better to create a
# valid user before running test cases and use it's credentials
default_user = env_file_content['default_user']
default_password = env_file_content['default_password']