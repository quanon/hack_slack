from config import load_config
from slackclient import SlackClient


def create_slack_client():
  config = load_config()
  slack_client = SlackClient(config['api_token'])

  return slack_client
