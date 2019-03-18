import os
import json

if os.environ.get("CONFIG_STRING"):
    env_file_content = json.loads(os.environ.get("CONFIG_STRING"))
else:
    config_file = 'auto_framework/src/resources/.config.json'
    env_file_content = json.load(open(os.path.abspath(config_file)))