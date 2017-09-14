from argparse import ArgumentParser
from client import create_slack_client
from config import load_config
import itertools
import sys

parser = ArgumentParser()
parser.add_argument('--types')
args = parser.parse_args()

if args.types:
  types = args.types
else:
  types = 'all'

if __name__ == '__main__':
  slack_client = create_slack_client()
  config = load_config()
  members = slack_client.api_call('users.list')['members']
  member = next(filter(lambda m: m['name'] == config['user'], members), None)

  if not member:
    sys.exit()

  for page in itertools.count(1):
    files = slack_client.api_call(
      'files.list', user=member['id'], page=page, types=types)['files']

    if not files:
      break

    for file in files:
      print(file['title'])
      slack_client.api_call('files.delete', file=file['id'])
