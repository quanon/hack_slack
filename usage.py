from argparse import ArgumentParser
from client import create_slack_client
from matplotlib import pyplot as plt
from operator import attrgetter
from prettytable import PrettyTable
import humanize
import itertools

parser = ArgumentParser()
parser.add_argument('--format')
args = parser.parse_args()

if args.format:
  format = args.format
else:
  format = 'table'


class Usage:
  def __init__(self, name):
    self.name = name
    self.count = 0
    self.size = 0

  def add_size(self, size):
    self.count += 1
    self.size += size

  def humanized_size(self):
    return humanize.naturalsize(self.size)


if __name__ == '__main__':
  slack_client = create_slack_client()
  members = slack_client.api_call('users.list')['members']
  usage_list = []

  for member in members:
    usage = Usage(member['name'])

    for page in itertools.count(1):
      files = slack_client.api_call(
        'files.list', user=member['id'], page=page)['files']

      if not files:
        break

      for file in files:
        usage.add_size(file['size'])

    usage_list.append(usage)

  usage_list.sort(key=attrgetter('size'), reverse=True)

  if format == 'graph':
    x = list(range(1, len(usage_list) + 1))
    labels = [u.name for u in usage_list]
    y = [round(u.size / 1024) for u in usage_list]
    plt.figure(figsize=(16, 8))
    plt.bar(x, y, align='center')
    plt.xticks(x, labels, rotation='vertical')
    plt.xlabel('user')
    plt.ylabel('usage (KB)')
    plt.tight_layout()
    plt.savefig('usage.png')
  else:
    table = PrettyTable(['username', 'usage', 'count'])
    table.align = 'r'

    for usage in usage_list:
      table.add_row([usage.name, usage.humanized_size(), usage.count])

    print(table)
