import json
import os


def load_config():
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  with open(config_path) as json_data:
    config = json.load(json_data)

  return config
