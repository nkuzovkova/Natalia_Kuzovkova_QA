import json
import os

env_file = os.environ.get('ENV_FILE') if os.environ.get('ENV_FILE') else ".qa.env"
global_config_file = 'resources/%s.json' % env_file
env_file_content = json.load(open(os.path.abspath(global_config_file)))

server = os.environ.get('server') if os.environ.get('server') else env_file_content['default_server']
login = env_file_content['default_login']
login_url = server + login

